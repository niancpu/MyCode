import tools.tool_models
from tools.registry import ToolRegister
from utils import log

# from tools.search import TavilySearch
# search_tool=TavilySearch()
# registry=ToolRegister()
# registry.register(name="search",
#                   description="基于tavily的搜索工具",
#                   func=search_tool.search
#                   )
log.warning("当前尚未注册Serach Tool")


add_schema=tools.tool_models.Add.model_json_schema()

registry=ToolRegister()
registry.register(
    name="add",
    description="加法函数",
    func=tools.tool_models.add_func,
    input_schema=add_schema
    )
toos_list=registry.all_tools()
log.debug("注册之后显示的是："+str(toos_list))

