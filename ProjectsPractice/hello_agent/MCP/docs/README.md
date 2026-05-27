# 手写 MCP - 简陋快速版

> 目标:不依赖 `mcp` SDK,自己用 JSON-RPC over stdio 撸一个最小可用的 Server + Client。
> 类比锚点:你的 `../ReAct/` 工程,本文档反复引用其中的模块对照。

---

## 一、一句话本质

**MCP = 把"工具表 + 工具实现"从你 Agent 的进程里拆出去,变成另一个进程,通过 JSON-RPC 2.0 跨进程喊话。**

ReAct 里你直接 `tool_register.tools[action]["func"](query)` —— 同进程函数调用。
MCP 里你 `client.call_tool(action, {"query": query})` —— 子进程 stdio 上的 RPC。

仅此而已。其它的 framing、握手、schema,都是为这件事服务的脚手架。

---

## 二、与你的 ReAct 的逐层映射

| ReAct 里的层                                 | MCP 里对应                                | 为什么变成这样                               |
| ------------------------------------------- | --------------------------------------- | --------------------------------------- |
| `register.py / ToolRegister`                | **Server 进程本身**                        | 注册表搬到了另一个进程里,通过 `tools/list` 暴露 |
| `ToolRegister.all_tools()` 返回 dict          | Server 响应 `tools/list` 返回的 `tools[]` | 必须加 `inputSchema`(跨进程不能靠 Python 类型) |
| `ToolRegister.tools[name]["func"](query)` 调用 | Client 发 `tools/call` 请求               | 同进程函数调用 → 跨进程 RPC                    |
| `search.py / TavilySearch`(真正的工具实现)        | Server 端注册的工具函数                       | 实现本身不变,变的是"谁来调它"                  |
| `loop.py / Loop`(LLM + 决策 + 调工具)             | **MCP Host**(你的 Agent / Claude Desktop) | Host 决定调什么、Server 只负责被调            |
| `observation.py / Observation`                | Host 自己的事,跟 MCP 无关                     | MCP 只管"工具调用",不管"调完怎么消化"           |
| `llm_call.py / LLMCall`                        | Host 自己的事,跟 MCP 无关                     | 同上                                     |
| ——(没有)                                     | **传输层**:stdin/stdout 字节流              | 同进程不需要,跨进程必须有                     |
| ——(没有)                                     | **协议层**:JSON-RPC 2.0                   | 同上                                     |
| ——(没有)                                     | **握手**:`initialize` + `capabilities`    | 跨进程要先协商"你支持啥"                     |

### 几个一眼看穿的对照

**ReAct 的工具注册**
```python
register.register("tavily_search", "联网搜索", TavilySearch().search)
```

**等价 MCP Server 暴露**
```json
{"jsonrpc":"2.0","id":1,"result":{"tools":[
  {"name":"tavily_search","description":"联网搜索",
   "inputSchema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}}
]}}
```
↑ 多了 `inputSchema`,因为对端不是 Python,不能靠类型推断,必须用 JSON Schema 描述参数。

**ReAct 的工具调用**
```python
func = tool_register.tools[action]["func"]
result = func(query)
```

**等价 MCP 请求**
```json
{"jsonrpc":"2.0","id":2,"method":"tools/call",
 "params":{"name":"tavily_search","arguments":{"query":"今天天气"}}}
```

**等价 MCP 响应**
```json
{"jsonrpc":"2.0","id":2,"result":{"content":[
  {"type":"text","text":"搜索结果:..."}
]}}
```

---

## 三、协议骨架(只需要会三个 method)

Server 必须响应:

1. **`initialize`** —— 握手。回报 `protocolVersion`、`capabilities`(声明自己支持 `tools`)、`serverInfo`。
2. **`tools/list`** —— 返回工具清单(参考上一节)。
3. **`tools/call`** —— 执行工具,返回 `content` 数组。

另外:客户端在握手完成后会发一条 **notification** `notifications/initialized` —— **没有 `id` 字段,不要回**。

消息 framing(stdio 模式):**每条 JSON 一行,`\n` 分隔**。

---

## 四、典型对话顺序

```
Client                                Server
  │  initialize ───────────────────────▶
  │  ◀─────────── result(capabilities)
  │  notifications/initialized ───────▶  (不回)
  │  tools/list ───────────────────────▶
  │  ◀─────────── result(tools[])
  │  tools/call ───────────────────────▶
  │  ◀─────────── result(content[])
  │  ...继续 tools/call...
```

把这个流程跟 ReAct 的 `Loop.run_loop` 对照看:ReAct 没有前两步(握手 + 列工具),因为同进程时工具表是直接传进 `run_loop` 的参数 `tools_desc` 和 `tool_register`。MCP 把这两样东西"网络化"了。

---

## 五、必踩的坑(先写在前面,免得调一天)

1. **日志绝对不能写 `stdout`**
   stdio 模式下 stdout 是协议通道。`print("debug...")` 一进去客户端直接 JSON 解析失败。
   → 所有日志一律 `print(..., file=sys.stderr)`,或者用 `logging` 配 `StreamHandler(sys.stderr)`。

2. **必须 flush**
   Python 的 `sys.stdout` 在 pipe 里默认全缓冲,你写完不 flush 对端永远收不到。
   → `sys.stdout.write(msg + "\n"); sys.stdout.flush()`,或开 `python -u`。

3. **notification 不要回**
   `notifications/initialized` 这种没有 `id` 的消息是单向通知,回了违反协议。判断方法:`"id" not in msg`。

4. **错误也要走 JSON-RPC error 格式**
   ```json
   {"jsonrpc":"2.0","id":2,"error":{"code":-32601,"message":"Method not found"}}
   ```
   不要把异常直接抛到 stdout。

5. **`tools/call` 的 result 必须包 `content` 数组**
   即使是纯文本,也要 `{"content":[{"type":"text","text":"..."}]}`。直接返回字符串客户端会报错。

---

## 六、建议的实现顺序

1. **先写 Server**,用 `print` 大法手动验证 —— 在终端跑起来,手敲一行 `initialize` JSON 喂给它的 stdin,看能不能正常返回。
2. **加 `tools/list` 和一个最简工具**(比如 `add(a, b)`),还是手敲 JSON 测。
3. **再写 Client** —— `subprocess.Popen` 把 server 拉起来,自动跑完整个握手 + 调用流程。
4. **最后把 ReAct 的 `Loop` 改造成 Host** —— 把原来 `tool_register.tools[action]["func"]` 那一行,替换成 `mcp_client.call_tool(action, parameter)`。**这一步做完,你的 ReAct 工具就跑在另一个进程里了。**

---

## 七、文件规划建议(本目录)

```
MCP/
├── server.py     # 自己手写的 server (响应三个 method)
├── client.py     # 自己手写的 client (subprocess + JSON-RPC 收发)
├── tools.py      # 具体工具实现 (类比 ReAct/search.py)
├── main.py       # demo: client 拉起 server,跑完整流程
└── README.md     # 本文档
```

`pyproject.toml` 里那个 `mcp` 依赖暂时用不上 —— 等手写版跑通了,再对照官方 SDK 看人家是怎么封装的,会更有体感。
