from client import MCPClient
from utils import get_logger
import logging

logger=get_logger(__name__)

def main():
    logger.info("程序启动")
    client=MCPClient(cmd=["python","server.py"])
    client.send_notification()
    client.initialize()
    


if __name__ == "__main__":
    main()
