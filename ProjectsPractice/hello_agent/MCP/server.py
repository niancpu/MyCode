from tools import registry
import sys
import json
from client import Msg,Resp
from dotenv import load_dotenv
from os import getenv
from logger_config import logger_config
import logging

logger_config()
logger=logging.getLogger(__name__)#根据文件名，同一个模块共用一个logger

load_dotenv()
tool_desc={}
try:
    VERSION=getenv("VERSION")
except:
    print("检查你的环境变量！")


def handle_msg(line:str)->Msg|None:
    try:
        msg=Msg(**json.loads(line.strip()))
    except Exception as e:
        send_resp(handle_error(None,-32700,"Parse error",f"不是合法json:{e}"))
    if not msg:
        return None
    if msg.jsonrpc == "2.0":#非对象比较用“==”
        error=handle_error(msg.id,-32600,"Invalid Request","jsonrpc 应当是 2.0")
        send_resp(error)
        return None
    if msg.method == "notifications/initialized":
        handle_initialized_notifications()
        return None
    #无需判断非notifacation是否有id，因为只要是没有id一律视为notifacation


    if msg.method == "initialize":
        assert msg.id is not None
        inited_resp=init_resp(msg.id)
        send_resp(inited_resp)
        return None
    return msg
    
    
def handle_error(id:int|None,code:int,type:str,desc:str|None=None)->Resp:
    error={"code":code,"message":f"{type}","data":f"{desc}"}
    err_msg=Resp(id=id,result=None,error=error)
    return err_msg

def list_capabilities()->dict[str,dict]:
    return {"tools":{}}



def send_resp(resp:Resp)->None:
    json_resp=resp.model_dump_json()
    sys.stdout.write(json_resp+"\n")
    sys.stdout.flush()

def handle_initialized_notifications()->None:
    log("notification")
    pass
    




class Server:
    def __init__(self):
        self.protocolVersion: dict = {"name":"nianzu's handmade MCP","version":VERSION}
        self.capabilities: dict | None= None #tools
        self.serverInfo: str = "2024-11-05"#name&version 

    def dispath(self,method:str)->dict|None:
        if method in tool_desc:
            return {method:tool_desc[method]}        
        else:
            return None
        
    def init_resp(self,id:int)->Resp:
        self.capabilities=list_capabilities()
        result={"protocolVersion":self.protocolVersion,"serverInfo":self.serverInfo,"capabilities":self.capabilities}
        resp=Resp(id=id,result=result)
        return resp

    def list_tools(self)->None:
        for i in registry.tools:
            tool_desc[i]=registry.tools[i]["description"]
        return None
    def run(self)->None:
        self.list_tools()
        for x in sys.stdin:#sys.stdin默认用\n作为分隔符
            msg=handle_msg(x)
            if msg is None:
                continue
            tool_desc=self.dispath(msg.method)
            if tool_desc is None:
                return None
        

def main():


            
        

if __name__=="__main__":
    main()


