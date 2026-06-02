from pydantic import BaseModel,ConfigDict,Field
from typing import Literal,Annotated,Any,Callable

class SearchResults(BaseModel):
    model_config=ConfigDict(extra="ignore")
    title:str
    content:str
    url:str
    score:float
    
class SearchResponse(BaseModel):
    model_config=ConfigDict(extra="ignore")
    result:SearchResults
    query:str
    response_time:float
    answer:str

class Msg(BaseModel):
    jsonrpc:str="2.0"
    id:int|None = None
    method:str
    params:dict[str,Any]|None=None

class TextContent(BaseModel):
    type:Literal["text"]="text"
    text:str|None=None

class ResourceContent(BaseModel):
    type:Literal["resource"]#表示这个字段的值只能是“resource”
    resource:dict|None=None

class ToolBackContent(BaseModel):
    content:list[
        Annotated[#第一个参数是真正的类型，后面是注释
            TextContent|ResourceContent,
            Field(discriminator="type")#表示区分TextContent|ResourceContent这个union的时候，根据对象的type字段
            ]
        ]|None=None

class ToolCallResp(BaseModel):
    jsonrpc:str="2.0"
    id:int|None
    result:ToolBackContent|None
    error:dict|None=None

class InputSchema(BaseModel):
    model_config=ConfigDict(extra="ignore")
    type:Literal["object"]
    properties:dict[str,dict]
    required:list[str]

class ToolItem(BaseModel):
    name:str
    description:str
    inputSchema:InputSchema
    func:Callable=Field(exclude=True)



class ListResult(BaseModel):
    tools:list[ToolItem]

class ToolListResp(BaseModel):
    jsonrpc:str="2.0"
    id:int|None
    result:ListResult
    error:dict|None=None

class InitResult(BaseModel):
    protocloVersion:str
    capabilities:dict[str,dict]
    serverInfo:dict[str,str]

class InitResp(BaseModel):
    jsonrpc:str="2.0"
    id:int|None
    result:InitResult

class ErrorContent(BaseModel):
    code:int
    message:str
    data:str

class ErrorResp(BaseModel):
    jsonrpc:str="2.0"
    id:int|None
    errorContent:ErrorContent



