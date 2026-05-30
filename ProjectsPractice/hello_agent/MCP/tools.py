from registry import ToolRegister
from tools.search import TavilySearch

search_tool=TavilySearch()
registry=ToolRegister()
registry.register(name="search",
                  description="基于tavily的搜索工具",
                  func=search_tool.search
                  )


