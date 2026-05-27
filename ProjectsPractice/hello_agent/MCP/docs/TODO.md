# TODO

## JSON-RPC 最小实现检查清单

这份清单不是“优化建议”，而是第一版要点名实现的功能。

### Server 必须实现的功能

- [ ] `serve()`：启动 stdio 循环，从 `stdin` 一行一行读 JSON-RPC 消息。
- [ ] `send_response(id, result)`：把成功响应写到 `stdout`，写完 `\n` 并 `flush()`。
- [ ] `send_error(id, code, message)`：把错误响应写到 `stdout`，写完 `\n` 并 `flush()`。
- [ ] `log(...)`：所有日志和异常细节只写到 `stderr`，不能污染 `stdout`。
- [ ] `handle_message(raw_line)`：解析一行 JSON；非法 JSON 返回 `-32700`，`id` 用 `null`。
- [ ] `validate_request(msg)`：检查 `jsonrpc`、`method`、`id`、`params` 这些基本字段；请求不合法返回 
- [ ] `dispatch(method, params)`：按 `method` 分发；未知 method 返回 `-32601`。
- [ ] `handle_initialize(params)`：实现 `initialize`，返回 `protocolVersion`、`capabilities.tools`、`serverInfo`。
- [ ] `handle_initialized_notification(params)`：处理 `notifications/initialized`；这是 notification，没有 `id`，不能回复。
- [ ] `handle_tools_list(params)`：实现 `tools/list`，返回工具清单 `tools`。
- [ ] `handle_tools_call(params)`：实现 `tools/call`，根据 `name` 和 `arguments` 调用工具。
- [ ] `call_tool(name, arguments)`：真正执行工具函数；工具不存在或参数错误时返回 `-32602`。
- [ ] `format_tool_result(value)`：把工具结果包装成 MCP 需要的 `{"content":[...]}`。
- [ ] `handle_internal_error(exc)`：内部异常返回 `-32603`，异常细节写到 `stderr`。
- [ ] 保证所有 JSON-RPC 响应里的 `id` 和请求里的 `id` 完全一致。

### Client 必须实现的功能

- [ ] `start_server()`：用 `subprocess.Popen` 启动 Server，并接管它的 `stdin`、`stdout`、`stderr`。
- [ ] `next_id()`：生成自增 JSON-RPC 请求 `id`。
- [ ] `send_request(method, params=None)`：发送带 `id` 的 JSON-RPC request，写 `\n` 并 `flush()`。
- [ ] `send_notification(method, params=None)`：发送不带 `id` 的 JSON-RPC notification，写完不等响应。
- [ ] `read_response(expected_id)`：从 Server 的 `stdout` 读一行响应，解析 JSON，并检查 `id` 是否匹配。
- [ ] `call(method, params=None)`：组合 `send_request()` + `read_response()`；如果响应里有 `error`，抛异常或返回错误。
- [ ] `initialize()`：调用 `initialize`，拿到 Server 的 `protocolVersion`、`capabilities`、`serverInfo`。
- [ ] `initialized()`：发送 `notifications/initialized`，不等待响应。
- [ ] `list_tools()`：调用 `tools/list`，拿到可用工具清单。
- [ ] `call_tool(name, arguments)`：调用 `tools/call`，传入工具名和参数，返回 `content`。
- [ ] `close()`：结束子进程，关闭管道，避免 Server 残留。
- [ ] 第一版主流程必须跑通：`start_server()` -> `initialize()` -> `initialized()` -> `list_tools()` -> `call_tool(...)`。
