import sys
import json
from models import InitResp, Msg,ToolListResp,InitResult,ErrorContent,ErrorResp,ToolItem,InputSchema,ListResult
from dotenv import load_dotenv
from os import getenv
import logging
from utils import get_logger
from tools.tool_register import registry

log=get_logger(__name__)
log=logging.getLogger(__name__)#根据文件名，同一个模块共用一个logger

load_dotenv()
tool_desc={}


try:
    VERSION=getenv("VERSION")
except:
    print("检查你的环境变量！")

class Server:
    def __init__(self):
        self.protocolVersion: str = "2024-11-05"
        self.capabilities: dict ={"tools":{}} #tools
        self.serverInfo: dict = {"name":"nianzu's handmade MCP","version":VERSION}#name&version 

    def dispath(self,msg:Msg)->dict|None:
        method=msg.method
        if method =="toos/call":
            return {method:tool_desc[method]}        
        elif method == "tools/list":
            return None
        elif msg.method == "initialize":
            assert msg.id is not None
            inited_resp=self.init_resp(msg.id)
            self.send_resp(InitResp.model_dump_json(inited_resp))
            return None
        if msg.method == "notifications/initialized":
            self.handle_initialized_notifications(msg)
            return None

    
    # def call(self,params:dict)->dict:

                
    def init_resp(self,id:int)->InitResp:
        result=InitResult.model_validate({
            "protocolVersion":self.protocolVersion,
            "serverInfo":self.serverInfo,
            "capabilities":self.capabilities
            })
        init_resp=InitResp(id=id,result=result)
        return init_resp
        
    def handle_exception(self,id:int|None,code:int,type:str,level:str,desc:str|None=None)->None:
        error_content=ErrorContent.model_validate({"code":code,"message":f"{type}","data":f"{desc}"})
        err_msg=ErrorResp(id=id,errorContent=error_content)
        if level=="warning":
            log.warning(err_msg)
        elif level=="error":
            log.error(err_msg)
    
    # def assemble_vals(self,tool_desc,i):

    def send_resp(self,resp:str)->None:
        sys.stdout.write(resp+"\n")
        sys.stdout.flush()

    def handle_initialized_notifications(self,msg:Msg)->None:
        log.warning("notification",
                    str(msg))
        return None

    def list_tools(self)->ListResult:
        return ListResult(tools=registry.all_tools())
                    
    def handle_msg(self,line:str)->Msg|None:
        try:
            msg=Msg(**json.loads(line.strip()))
        except Exception as e:
            self.handle_exception(None,-32700,"Parse error",f"不是合法json:{e}","error")
        if not msg:
            return None
        if msg.jsonrpc != "2.0":#非对象比较用“==”
            self.handle_exception(msg.id,-32600,"Invalid Request","jsonrpc 应当是 2.0","error")
            return None
        #无需判断非notifacation是否有id，因为只要是没有id一律视为notifacation

        return msg

    def run(self)->None:
        self.list_tools()
        log.debug("list_tools",
                  str(self.list_tools))
        for x in sys.stdin:#sys.stdin默认用\n作为分隔符
            msg=self.handle_msg(x)
            log.debug("msg",
                      str(msg))
            if msg is None:
                continue
            log.info("成功接受message")
            tool_desc=self.dispath(msg)
            log.debug("tool_desc",
                      str(tool_desc))
            if tool_desc is None:
                return None
        

def main():


            
        

if __name__=="__main__":
    main()


