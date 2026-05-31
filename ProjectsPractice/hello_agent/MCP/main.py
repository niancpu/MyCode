from client import MCPClient

def main():
    client=MCPClient(cmd=["python","server.py"])
    client.send_notification()
    client.initialize()
    


if __name__ == "__main__":
    main()
