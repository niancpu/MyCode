from client import MCPClient
from utils import get_logger
from sys import executable
from tools.tool_models import Add
import asyncio

logger=get_logger(__name__)

async def run(client:MCPClient):
    client.send_notification()
    client.initialize()
    logger.info("===============================开始tools/list============================")
    resuslt=client.call("tools/list")
    logger.info(resuslt)
    logger.info("============================开始tools/call===============================")
    resp=client.call("tools/call",params={"a":1,"b":2})



if __name__ == "__main__":
    async def main():
        client=MCPClient(cmd=[executable,"server.py"])
        try:
            logger.info("开始运行代码")
            result=await asyncio.gather(
            asyncio.to_thread(run,client)
            )
        except (KeyboardInterrupt,RuntimeError) as e:
            logger.debug("进入main的except块")
            client.close()
    asyncio.run(main())