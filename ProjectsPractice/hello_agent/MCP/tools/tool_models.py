from pydantic import BaseModel

class Add(BaseModel):
    a:int
    b:int

def add(args:Add)->int:
    return args.a+args.b
