from pydantic import BaseModel,ConfigDict

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
    params:dict|None=None

class Resp(BaseModel):
    jsonrpc:str="2.0"
    id:int|None
    result:dict|None
    error:dict|None=None
