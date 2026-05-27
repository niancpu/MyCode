from tools import registry
import sys
import json
from client import Msg,Resp
from dotenv import load_dotenv
from os import getenv

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
    if msg.jsonrpc is not "2.0":
        error=handle_error(msg.id,-32600,"Invalid Request","jsonrpc 应当是 2.0")
        send_resp(error)
        return None
    if msg.method is "notification/initialized":
        handle_initialized_notifications()
        return None
    if msg.id is None:
        error=handle_error(msg.id,-32600,"Invalid Request","非notification消息返回体无id")
        send_resp(error)
        return None


        
    return msg
    
    
def handle_error(id:int|None,code:int,type:str,desc:str|None=None)->Resp:
    error={"code":code,"message":f"[{type}] {desc}"}
    err_msg=Resp(id=id,result=None,error=error)
    return err_msg

def init_resp(id:int)->Resp:
    capabilities=list_tools()
    serverInfo= {"name":"nianzu's handmade MCP","version":VERSION}
    result={"protocolVersion":"2.0","serverInfo":serverInfo,"capabilities":capabilities}
    resp=Resp(id=id,result=result)
    return resp

def send_resp(resp:Resp)->None:
    json_resp=resp.model_dump_json()
    sys.stdout.write(json_resp+"\n")
    sys.stdout.flush()

def handle_initialized_notifications()->None:
    log("notification")
    pass
    

def list_tools()->None:
    for i in registry.tools:
        tool_desc[i]=registry.tools[i]["description"]
    return None

def dispath(method:str)->dict|None:
    if method in tool_desc:
        return {method:tool_desc[method]}
    elif(method=="initialize"):
        assert msg.id is not None
        inited_resp=init_resp(msg.id)
        send_resp(inited_resp)
        return None
    else:
        return None


def main():
    list_tools()
    for x in sys.stdin:#sys.stdin默认用\n作为分隔符
        msg=handle_msg(x)
        if msg is None:
            continue



            
        

if __name__=="__main__":
    main()


