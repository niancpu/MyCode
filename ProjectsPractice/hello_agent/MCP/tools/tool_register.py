import tool_models
from tools.registry import ToolRegister
from tools.search import TavilySearch
from utils import get_logger

log=get_logger(__name__)

search_tool=TavilySearch()
registry=ToolRegister()
# registry.register(name="search",
#                   description="基于tavily的搜索工具",
#                   func=search_tool.search
#                   )
log.warning("当前尚未注册Serach Tool")

add_schema=tool_models.Add.model_json_schema()

registry=ToolRegister()
registry.register(
    name="add",
    description="加法函数",
    func=tool_models.Add,
    input_schema=add_schema
    )

