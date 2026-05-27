from llm_call import env_loader
from tavily import TavilyClient
from pydantic import BaseModel,ConfigDict
from typing import Optional,List,Any
from model import Search
TAVILY_API_KEY=env_loader("TAVILY_API_KEY")

client=TavilyClient(TAVILY_API_KEY)

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

class TavilySearch(Search):
    def search(self,query:str)->SearchResponse:
        response=client.search(
            query,
            auto_parameters=True,
            include_usage=True,
            include_answer=True
            )
        result:SearchResponse=SearchResponse(**response)
        return result




