from typing import Any,Callable
from models import ToolItem,InputSchema

class ToolRegister:
    def __init__(self) -> None:
        self.tools:list[ToolItem]=[]
    
    def register(self,name:str,description:str,func:Callable,input_schema:str)->None:
        item=ToolItem(name=name,description=description,func=func,inputSchema=InputSchema.model_validate(input_schema))

    def get_tool(self,name:str)->Callable|None:
        for i in self.tools:
            if i.name==name:
                return i.func
    
    def all_tools(self):
        return self.tools
    
    
