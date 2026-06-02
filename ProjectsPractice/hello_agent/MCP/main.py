from client import MCPClient
from utils import get_logger
from models import InputSchema
from sys import executable
from tools.tool_models import Add

logger=get_logger(__name__)

def main():
    logger.info("程序启动")
    client=MCPClient(cmd=[executable,"server.py"])
    client.send_notification()
    client.initialize()
    logger.info("=============================================================")
    resuslt=client.call("tools/list")
    logger.info(resuslt)
    logger.info("=============================================================")
    add=Add(a=1,b=2)
    resp=client.call("tools/call",params={"a":1,"b":2})
    content=resp
    client.close()
    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt or RuntimeError:
        pass