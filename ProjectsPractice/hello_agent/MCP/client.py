import subprocess
import json
from typing import Optional
from models import Resp,Msg


class server:
    def __init__(self,cmd:list[str]) -> None:
        self.proc=subprocess.Popen(
            cmd,
            bufsize=1,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.id:int=0
        self.protocolVersion: str | None = None
        self.capabilities: dict | None = None#tools
        self.serverInfo: dict | None = None#name&version
    
    def _next_id(self)->int:
        self.id+=1
        return self.id
    
    def _send_request(self,msg:Msg)->Resp:
        assert self.proc.stdin is not None
        assert self.proc.stdout is not None
        self.proc.stdin.write(json.dumps(msg)+"\n")
        self.proc.stdin.flush()
        try:
            line=self.proc.stdout.readline()
        except Exception as e:
            raise RuntimeError(f"stdout返回读取出错！{e}")from e
        if msg.id is None:
            raise RuntimeError("非notification消息返回体无id！")
        return self.read_response(msg.id,line)

    def send_notification(self)->None:
        notification=Msg(method="notification/initialized")
        assert self.proc.stdin is not None
        assert self.proc.stdout is not None
        self.proc.stdin.write(json.dumps(notification)+"\n")
        self.proc.stdin.flush()
    
    def read_response(self,id:int,response:str)->Resp:
        try:
            resp=Resp(**json.loads(response))
        except Exception as e:
            raise RuntimeError(f"未能成功解析返回的json，格式错误！{e}")from e
        if resp.id!=id:
            raise RuntimeError(f"id不匹配！")
        if resp.jsonrpc!="2.0":
            raise RuntimeError(f"jsonrpc版本号不对！")
        if resp.error is not None:
            raise RuntimeError(f"响应报错，报错如下：\n{json.dumps(resp.error)}")
        return resp
    
    def initialize(self):
        resp=self.call(method="initialize")
        result=resp.result
        if result is None:
            raise RuntimeError(f"initialize方法返回体不应为空！")
        self.protocolVersion=result["protocolVersion"]
        self.capabilities=result["capabilities"]
        self.serverInfo=result["serverInfo"]
        for k in [self.protocolVersion,self.capabilities,self.serverInfo]:
            if k is None:
                raise RuntimeError(f"initialize方法返回体值缺失！")
        

# {
#   "jsonrpc": "2.0",
#   "id": <请求里的 id>,
#   "result": {
#     "protocolVersion": "2024-11-05",
#     "capabilities": {
#       "tools": {}
#     },
#     "serverInfo": {
#       "name": "handmade-mcp",
#       "version": "0.1.0"
#     }
#   }
# }        

    def call(self,method:str,params:dict[str,str]|None=None)->Resp:
        if params is None:
            if(method is not "initialize"):
                raise RuntimeError(f"缺少参数！")

            msg=Msg(id=self._next_id(),method=method)
            return self._send_request(msg=msg)
        msg=Msg(method=method,params=params,id=self._next_id())
        return self._send_request(msg=msg)

    def close(self):
        if self.proc.poll() is None:
            assert self.proc.stdin is not None
            assert self.proc.stdout is not None
            self.proc.stdin.close()        
            self.proc.stdout.close()
            self.proc.terminate()
            self.proc.wait(timeout=5)                
        




