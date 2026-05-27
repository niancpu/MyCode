from loop import Loop,print_to_console
from register import ToolRegister
from search import TavilySearch

def main():
    # query=input("输入您的问题：")
    query="帮我研究一下现在华为手机哪一个版本最值得买"
    react_loop=Loop()
    tool_register=ToolRegister()
    search=TavilySearch()
    tool_register.register(
        name="search",
        description="""这是一个搜索工具，传入参数需要遵循的格式是
        `{{
            "query":"具体的查询内容"
        }}`
        """,
        func=search.search)
    tools_desc=tool_register.all_tools()
    print_to_console("tool_desc(raw_get)",str(tools_desc))

    react_loop.run_loop(query,max_rounds=5,tools_desc=tools_desc,tool_register=tool_register)

if __name__ == "__main__":
    main()
