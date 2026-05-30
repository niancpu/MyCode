from typing import Any,Callable
from models import ToolItem,InputSchema

class ToolRegister:
    def __init__(self) -> None:
        self.tools:list[ToolItem]=[]
    
    def register(self,name:str,description:str,func:Callable,input_schema:InputSchema)->None:
        item=ToolItem(name=name,description=description,func=func)

    def get_tool(self,name:str)->Callable|str:
        if self.tools[name]:
            return self.tools[name]["func"]
        else:
            return "此工具不存在！"
    
    def all_tools(self)->dict[str,str]:
        all_tools={}
        for k,v in self.tools.items():
            all_tools.update({k:v["description"]})
        return all_tools
    
    
