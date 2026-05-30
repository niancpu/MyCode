import tool_models
from registry import ToolRegister
from tools.search import TavilySearch
from logger_config import logger_config,logging

logger_config()
log=logging.getLogger(__name__)

search_tool=TavilySearch()
registry=ToolRegister()
# registry.register(name="search",
#                   description="基于tavily的搜索工具",
#                   func=search_tool.search
#                   )
log.warning()

add_schema=tool_models.Add.model_json_schema()

