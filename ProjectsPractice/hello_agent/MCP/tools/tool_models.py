from pydantic import BaseModel

class Add(BaseModel):
    a:int
    b:int
    c:int=0
def add(args:Add)->int:
    return args.a+args.b
