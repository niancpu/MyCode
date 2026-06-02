import threading
import subprocess
import json
from typing import Any
from models import InitResp,ToolCallResp,ToolListResp,Msg
import asyncio

from utils import log

class MCPClient:
    def __init__(self,cmd:list[str]) -> None:
        self.proc=subprocess.Popen(
            cmd,
            bufsize=1,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        self.id:int=0
    
    def _next_id(self)->int:
        self.id+=1
        return self.id
    
    def _send_request(self,msg:Msg)->dict:
        assert self.proc.stdin is not None
        assert self.proc.stdout is not None
        log.debug(Msg.model_dump_json(msg))
        self.proc.stdin.write(Msg.model_dump_json(msg)+"\n")
        self.proc.stdin.flush()
        line=self.proc.stdout.readline()
        log.debug(line)
        if not line:
            retcode=self.proc.poll() #防止子进程异常退出产生异常空回复
            if retcode is not None:
                raise RuntimeError(f"mcp server子进程返回，返回码{retcode}")
            else:
                log.exception("子进程活着但是异常回复")
        if line !="\n":
            assert msg.id is not None
            return self._read_response(msg.id,line)
        else:
            return {}

    def send_notification(self)->None:
        notification=Msg(method="notifications/initialized")
        assert self.proc.stdin is not None
        assert self.proc.stdout is not None
        self.proc.stdin.write(Msg.model_dump_json(notification)+"\n")
        self.proc.stdin.flush()
    
    def _read_response(self,id:int,response:str)->dict:
        try:
            log.debug(repr(response[:80]))   # 看原始字符串前80个字符
            resp=json.loads(response)
            log.debug(resp)
            log.debug(type(resp))
        except Exception as e:
            raise RuntimeError(f"未能成功解析返回的json，格式错误！{e}")from e
        if resp["id"]!=id:
            raise RuntimeError(f"id不匹配！")
        if resp["jsonrpc"]!="2.0":
            raise RuntimeError(f"jsonrpc版本号不对！")
        if resp["error"]:
            raise RuntimeError(f"响应报错，报错如下：\n{json.dumps(resp.error)}")
        return resp
    
    
    def initialize(self):
        resp=self.call(method="initialize")
        result=resp["result"]
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

    def call(self,method:str,params:dict[str,Any]|None=None)->dict:
        if params is None:
            params={}

            msg=Msg(id=self._next_id(),method=method)
            return self._send_request(msg=msg)
        msg=Msg(method=method,params=params,id=self._next_id())
        return self._send_request(msg=msg)

    def close(self):
        if self.proc.poll() is None:
            assert self.proc.stdin is not None
            assert self.proc.stdout is not None
            self.proc.terminate()   
            self.proc.wait(timeout=5)  #等待5秒之后关管道，防止立刻关导致
            log.debug(self.proc.stdin)
            log.debug(self.proc.stdout)
            self.proc.stdin.close()    
            self.proc.stdout.close()