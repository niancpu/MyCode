import sys
import json
from models import InitResp, Msg,ToolListResp,InitResult,ErrorContent,ErrorResp,ToolItem,InputSchema,ListResult,ToolCallResp,ToolBackContent
from dotenv import load_dotenv
from os import getenv
from utils import get_logger
from tools.tool_register import registry
from typing import Any

log=get_logger(__name__)
load_dotenv()

try:
    VERSION=getenv("VERSION")
except:
    print("检查你的环境变量！")

class Server:
    def __init__(self):
        self.protocolVersion: str = "2024-11-05"
        self.capabilities: dict ={"tools":{}} #tools
        self.serverInfo: dict = {"name":"nianzu's handmade MCP","version":VERSION}#name&version
 
    def dispath(self,msg:Msg)->str|None:
        method=msg.method
        if (msg.params is None)and(msg.id is None):
            if msg.method == "notifications/initialized":
                self.handle_initialized_notifications(msg)
                return None
            else:
                log.error("非notifications方法param字段为空")
        else:
            assert msg.id and msg.params is not None
            if method =="tools/call":
                resp=self.tool_call(id=msg.id,params=msg.params)
            elif method == "tools/list":
                tool_list:ListResult=self.list_tools()
                resp=self.get_list_resp(msg.id,tool_list)
            elif msg.method == "initialize":
                assert msg.id is not None
                resp=self.init_resp(msg.id)
            return str(resp)
    
    def tool_call(self,params:dict[str,Any],id:int)->ToolCallResp|None:
        tool_list=self.list_tools()
        for i in tool_list.tools:#这里不能for i in tool_list是因为Pydantic 的 BaseModel 实现了 __iter__，遍历它等价于遍历 .model_dump() 的键值对而不是遍历.tools属性
            if params["name"] in i.name:
                result:ToolBackContent=i.func(params["property"])
                return ToolCallResp(result=result,id=id)
            else:
                return None


            
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
        log.warning("notification"+
                    str(msg))
        return None

    def list_tools(self)->ListResult:
        return ListResult(tools=registry.all_tools())

    def get_list_resp(self,id:int,tool_list:ListResult)->ToolListResp:
        return ToolListResp(id=id,result=tool_list)

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
        log.debug("list_tools："+
                  str(self.list_tools()))
        for x in sys.stdin:#sys.stdin默认用\n作为分隔符
            log.info("Server接收messages")
            msg=self.handle_msg(x)
            log.debug("msg"+
                      str(msg))
            if msg is None:
                continue
            log.info("成功接受message")
            resp=self.dispath(msg)
            log.debug(resp)
            if resp is not None:
                self.send_resp(resp=resp)
                log.info("server返回response")
        

def main():
    server=Server()
    server.run()

if __name__=="__main__":
    main()


