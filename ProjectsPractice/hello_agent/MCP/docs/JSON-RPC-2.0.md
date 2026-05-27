# JSON-RPC 2.0 快速上手

> 这份文档只服务于本目录的目标：不用 MCP SDK，手写一个最小可用的 MCP Server + Client。
>
> 你不用先啃完整规范。先把下面几件事搞清楚，就能开始写代码。

官方规范在这里：<https://www.jsonrpc.org/specification>

---

## 1. 先记住一句话

JSON-RPC 就是用 JSON 表示一次“远程函数调用”。

在同一个 Python 进程里，你可能这样调工具：

```python
result = add(a=1, b=2)
```

换成 JSON-RPC，就是把这次调用写成一条 JSON 消息发给另一个进程：

```json
{"jsonrpc":"2.0","id":1,"method":"add","params":{"a":1,"b":2}}
```

对方执行完，再回一条 JSON：

```json
{"jsonrpc":"2.0","id":1,"result":3}
```

这就是 JSON-RPC 的核心。

---

## 2. 它在 MCP 里干什么

MCP 基于 JSON-RPC 2.0。

你现在要手写 MCP，可以先把它理解成：

```text
Client / Host                    Server
    发 JSON-RPC 请求   ----->      收到 method，执行对应逻辑
    收 JSON-RPC 响应   <-----      返回 result 或 error
```

在本项目里，MCP 最小版只需要会 3 个 method：

| method | 作用 | 你要做什么 |
| --- | --- | --- |
| `initialize` | 握手 | Server 返回自己支持什么能力 |
| `tools/list` | 列工具 | Server 返回工具清单 |
| `tools/call` | 调工具 | Server 执行工具并返回结果 |

还有一个特殊消息：

```json
{"jsonrpc":"2.0","method":"notifications/initialized"}
```

它没有 `id`，所以是 notification。Server 收到后不要回复。

---

## 3. 一条请求长什么样

请求对象固定是一个 JSON object：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "add",
    "arguments": {"a": 1, "b": 2}
  }
}
```

字段含义：

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `jsonrpc` | 是 | 固定写 `"2.0"` |
| `id` | 否 | 请求编号。响应要用同一个 `id` 回来 |
| `method` | 是 | 要调用的方法名 |
| `params` | 否 | 参数，可以是 object，也可以是 array |

你手写 MCP 时，建议 `params` 全部用 object。可读，也不怕参数顺序变。

---

## 4. 一条成功响应长什么样

请求里有 `id`，Server 就要回复。

成功时返回 `result`：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {"type": "text", "text": "3"}
    ]
  }
}
```

注意两点：

- 响应里的 `id` 必须和请求里的 `id` 一样。
- `result` 和 `error` 只能出现一个，不能同时出现。

MCP 的 `tools/call` 结果要包成 `content` 数组：

```json
{
  "content": [
    {"type": "text", "text": "工具返回的文本"}
  ]
}
```

不要直接返回：

```json
"工具返回的文本"
```

很多 MCP Client 会不认这种裸字符串。

---

## 5. Notification：没有 id 就不要回

没有 `id` 的请求叫 notification。

```json
{"jsonrpc":"2.0","method":"notifications/initialized"}
```

规则很简单：

- 没有 `id`，Server 不回复。
- 即使处理失败，也不回复。
- 如果你回复了，Client 可能会认为协议乱了。

判断方式：

```python
is_notification = "id" not in msg
```

不要用 `msg.get("id") is None` 判断。`id: null` 和没有 `id` 不是一回事。

---

## 6. 错误响应长什么样

失败时返回 `error`：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

你现在先记这几个错误码就够了：

| code | 含义 | 什么时候用 |
| --- | --- | --- |
| `-32700` | Parse error | 收到的不是合法 JSON |
| `-32600` | Invalid Request | JSON 合法，但不是合法 JSON-RPC 请求 |
| `-32601` | Method not found | `method` 不存在 |
| `-32602` | Invalid params | 参数缺失、类型不对 |
| `-32603` | Internal error | 方法内部异常 |

一个小工具函数就够用：

```python
def make_error(id_: int | str | None, code: int, message: str, data: object = None) -> dict:
    error = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": id_, "error": error}
```

---

## 7. stdio 模式怎么传

JSON-RPC 只规定消息长什么样，不规定怎么传。

我们手写 MCP 先用最简单的 stdio：

```text
stdin  读请求
stdout 写响应
stderr 写日志
```

本项目建议用“一行一条 JSON”：

```text
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":2}}}
```

Server 每次从 `stdin` 读一行，解析 JSON，处理后往 `stdout` 写一行 JSON。

写完必须 flush：

```python
sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
sys.stdout.flush()
```

日志不能写 stdout：

```python
print("debug info", file=sys.stderr)
```

因为 stdout 是协议通道。你往 stdout 打一行 debug，Client 就会拿它当 JSON-RPC 消息解析，然后炸掉。

---

## 8. MCP 最小对话流程

真正跑起来时，大概是这个顺序：

```text
Client -> Server
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}

Server -> Client
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"handmade-mcp","version":"0.1.0"}}}

Client -> Server
{"jsonrpc":"2.0","method":"notifications/initialized"}

Client -> Server
{"jsonrpc":"2.0","id":2,"method":"tools/list"}

Server -> Client
{"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"add","description":"Add two numbers","inputSchema":{"type":"object","properties":{"a":{"type":"number"},"b":{"type":"number"}},"required":["a","b"]}}]}}

Client -> Server
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":2}}}

Server -> Client
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"3"}]}}
```

这里最容易漏的是 `notifications/initialized`：它没有 `id`，所以 Server 不要回。

---

## 9. Server 最小结构

先不用写得很抽象。一个 dispatch 函数就够。

```python
import json
import sys
import traceback
from typing import Any

JsonRpcId = int | str | None
JsonRpcMsg = dict[str, Any]


def write_msg(msg: JsonRpcMsg) -> None:
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def make_error(id_: JsonRpcId, code: int, message: str, data: Any = None) -> JsonRpcMsg:
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": id_, "error": error}


def handle_initialize(msg: JsonRpcMsg) -> JsonRpcMsg:
    return {
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "handmade-mcp", "version": "0.1.0"},
        },
    }


def handle_tools_list(msg: JsonRpcMsg) -> JsonRpcMsg:
    return {
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "tools": [
                {
                    "name": "add",
                    "description": "Add two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"},
                        },
                        "required": ["a", "b"],
                    },
                }
            ]
        },
    }


def handle_tools_call(msg: JsonRpcMsg) -> JsonRpcMsg:
    params: dict[str, Any] = msg.get("params") or {}
    name: str | None = params.get("name")
    arguments: dict[str, Any] = params.get("arguments") or {}

    if name != "add":
        return make_error(msg["id"], -32601, "Tool not found")

    try:
        result = arguments["a"] + arguments["b"]
    except Exception as exc:
        return make_error(msg["id"], -32602, "Invalid params", str(exc))

    return {
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "content": [
                {"type": "text", "text": str(result)}
            ]
        },
    }


def handle_msg(msg: Any) -> JsonRpcMsg | None:
    if not isinstance(msg, dict):
        return make_error(None, -32600, "Invalid Request")

    if msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        return make_error(msg.get("id"), -32600, "Invalid Request")

    is_notification: bool = "id" not in msg
    method: str = msg["method"]

    if is_notification:
        # MCP 的 notifications/initialized 就走这里。
        # notification 按协议不回复。
        return None

    if method == "initialize":
        return handle_initialize(msg)
    if method == "tools/list":
        return handle_tools_list(msg)
    if method == "tools/call":
        return handle_tools_call(msg)

    return make_error(msg["id"], -32601, "Method not found")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        msg: Any
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            write_msg(make_error(None, -32700, "Parse error"))
            continue

        resp: JsonRpcMsg | None
        try:
            resp = handle_msg(msg)
        except Exception:
            traceback.print_exc(file=sys.stderr)
            resp = make_error(msg.get("id") if isinstance(msg, dict) else None, -32603, "Internal error")

        if resp is not None:
            write_msg(resp)


if __name__ == "__main__":
    main()
```

这段代码不是最终架构，但足够你先跑通 MCP 的协议感觉。

---

## 10. Client 最小结构

Client 做三件事：

1. 启动 Server 子进程。
2. 往 Server 的 stdin 写 JSON-RPC 请求。
3. 从 Server 的 stdout 读 JSON-RPC 响应，并按 `id` 匹配。

最小同步版可以先这样写：

```python
import itertools
import json
import subprocess
import sys
from typing import Any, Iterator

JsonRpcMsg = dict[str, Any]


class JsonRpcClient:
    proc: subprocess.Popen[str]
    _ids: Iterator[int]

    def __init__(self, cmd: list[str]) -> None:
        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._ids = itertools.count(1)

    def send(self, msg: JsonRpcMsg) -> None:
        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def read(self) -> JsonRpcMsg:
        assert self.proc.stdout is not None
        line: str = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("server closed stdout")
        return json.loads(line)

    def call(self, method: str, params: dict[str, Any] | None = None) -> Any:
        req_id: int = next(self._ids)
        msg: JsonRpcMsg = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            msg["params"] = params

        self.send(msg)
        resp = self.read()

        if resp.get("id") != req_id:
            raise RuntimeError(f"id mismatch: expected {req_id}, got {resp.get('id')}")

        if "error" in resp:
            raise RuntimeError(resp["error"])

        return resp["result"]

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        msg: JsonRpcMsg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self.send(msg)


if __name__ == "__main__":
    client = JsonRpcClient([sys.executable, "server.py"])

    print(client.call("initialize", {}))
    client.notify("notifications/initialized")
    print(client.call("tools/list"))
    print(client.call("tools/call", {"name": "add", "arguments": {"a": 1, "b": 2}}))
```

这个版本一次只发一个请求，然后立刻等响应。先够用。

后面如果要支持并发请求，再加 reader 线程和 pending 表。

---

## 11. 手写时最容易踩的坑

### 11.1 stdout 被日志污染

错误写法：

```python
print("server started")
```

正确写法：

```python
print("server started", file=sys.stderr)
```

stdio 模式下，stdout 只能放 JSON-RPC 消息。

### 11.2 忘记 flush

错误写法：

```python
sys.stdout.write(json.dumps(resp) + "\n")
```

正确写法：

```python
sys.stdout.write(json.dumps(resp) + "\n")
sys.stdout.flush()
```

### 11.3 notification 回了响应

错误逻辑：

```python
if method == "notifications/initialized":
    return {"jsonrpc": "2.0", "result": "ok", "id": None}
```

正确逻辑：

```python
if "id" not in msg:
    return None
```

### 11.4 `result` 和 `error` 同时出现

不要这样：

```json
{"jsonrpc":"2.0","id":1,"result":null,"error":{"code":-32603,"message":"failed"}}
```

成功就只有 `result`，失败就只有 `error`。

### 11.5 `id` 没原样返回

请求：

```json
{"jsonrpc":"2.0","id":"abc","method":"ping"}
```

响应必须是：

```json
{"jsonrpc":"2.0","id":"abc","result":"pong"}
```

不能把 `"abc"` 改成 `1`，也不能漏掉。

---

## 12. 你现在可以忽略的东西

为了先把 MCP 跑起来，这些可以晚点再看：

- Batch：一个数组里塞多个请求。
- OpenRPC：JSON-RPC 的接口描述文档。
- HTTP / WebSocket 绑定：现在先用 stdio。
- 双向请求：Server 主动调 Client，最小 MCP 工具调用先用不上。
- 流式进度：以后做长任务再加。
- 认证鉴权：本地父子进程 stdio 先不处理。

先不要把这些塞进第一版。第一版只要把 `initialize`、`tools/list`、`tools/call` 跑通。

---

## 13. 最小实现检查清单

具体 TODO 已抽到 [`TODO.md`](TODO.md)。第一版照着里面的 Server / Client 功能清单实现即可。

---

## 14. 跟 README 的关系

README 里说：

> MCP = 把“工具表 + 工具实现”从 Agent 的进程里拆出去，变成另一个进程，通过 JSON-RPC 2.0 跨进程喊话。

这份文档只补一个东西：JSON-RPC 这层“喊话”到底怎么喊。

你可以按这个顺序写：

1. `server.py`：先硬编码 `initialize`、`tools/list`、`tools/call`。
2. `client.py`：启动 server，完成握手，调一次工具。
3. `tools.py`：把工具函数从 server 里拆出去。
4. `main.py`：跑完整 demo。
5. 再回头优化错误处理、工具注册表、并发读取。

先跑通，再变干净。
