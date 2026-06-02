from client import MCPClient
from sys import executable,stderr
from tools.tool_models import Add
import asyncio
from utils import log
import tools.tool_register
 
def run(client:MCPClient):
    client.send_notification()
    client.initialize()
    log.info("===============================开始tools/list============================")
    resuslt=client.call("tools/list")
    log.info(resuslt)
    log.info("============================开始tools/call===============================")
    resp=client.call("tools/call",params={"a":1,"b":2})
    log.debug(resp)


if __name__ == "__main__":
    async def main():
        client=MCPClient(cmd=[executable,"server.py"])
        try:
            log.info("开始运行代码")
            result=await asyncio.gather(
            asyncio.to_thread(run,client)
            )
            log.debug("keyinterrupt")
        except (KeyboardInterrupt,RuntimeError,BaseException):
            log.exception("接受KeyInterrupt，进入main的except块")#log.exception会带上原始traceback
            # client.close()
    asyncio.run(main())