from pydantic import BaseModel
from models import ToolBackContent,TextContent

class Add(BaseModel):
    a:int
    b:int        

def add_func(args:Add)->ToolBackContent:
    content=TextContent(text=str(args.a+args.b))
    result=ToolBackContent(content=[
        content
    ])
    return result