from pydantic import BaseModel
from models import ToolBackContent,TextContent,ResourceContent

class Add(BaseModel):
    a:int
    b:int
    c:int=0
def add(args:Add)->ToolBackContent:
    content=TextContent(text=str(args.a+args.b))
    result=ToolBackContent(content=[
        content
    ])
    return result