from typing import Any,Callable
from models import ToolItem,InputSchema
from tools.tool_models import  Add

class ToolRegister:
    def __init__(self) -> None:
        self._tools:list[ToolItem]=[]
    
    def register(self,name:str,description:str,func:Callable,input_schema:dict[str,Any])->None:
        item=ToolItem(name=name,description=description,func=func,inputSchema=InputSchema.model_validate(input_schema),model=Add)

    def get_tool(self,name:str)->Callable|None:
        for i in self._tools:
            if i.name==name:
                return i.func
    
    def all_tools(self):
        return self._tools
    
    
