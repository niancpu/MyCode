from dotenv import dotenv_values
from tavily import TavilyClient
from models import SearchResponse
TAVILY_API_KEY=dotenv_values()["TAVILY_API_KEY"]

client=TavilyClient(TAVILY_API_KEY)

class TavilySearch():
    def search(self,query:str)->SearchResponse:
        response=client.search(
            query,
            auto_parameters=True,
            include_usage=True,
            include_answer=True
            )
        result:SearchResponse=SearchResponse(**response)
        return result




