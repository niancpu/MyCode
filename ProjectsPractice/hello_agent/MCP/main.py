from client import MCPClient
from utils import get_logger
import logging
from sys import executable

logger=get_logger(__name__)

def main():
    logger.info("程序启动")
    client=MCPClient(cmd=[executable,"server.py"])
    client.send_notification()
    client.initialize()
    client.close()
    


if __name__ == "__main__":
    main()
