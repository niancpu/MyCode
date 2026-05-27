from typing import Any,Callable
from llm_call import LLMCall
import json
from search import TavilySearch,SearchResponse
from observation import Observation
from utils import dumps

THOUGHT_AND_ACTION="""
# ROLE
你是一个拥有工具执行能力的助手
你的可执行工具如下
{tools}
用户的问题是：{question}
# HISTORY
{history}
# FORMAR
你的回答需要遵从以下两种格式之一，任务未完成：
`{{
    "think":"思考的具体内容..."
    "action":"你决定使用的工具的名称"
    "parameter":"你为工具传入的参数"
}}`
如果任务已经完成或者已经得到结果：
`["finish","具体的内容..."]`
"""
class Loop:
    def __init__(self):
        self.llm_client=LLMCall()
        self.observation=Observation()
    def run_loop(self,user_input:str,max_rounds:int,tools_desc:dict[str,str],tool_register)->None:

        content=THOUGHT_AND_ACTION.format(
            tools=dumps(tools_desc),
            question=user_input,
            history="无",
        )
        messages=[{"role":"user","content":content}]
        history="# Initial instrutions & System Prompt"+"\n"+str(content)

        for i in range(1,max_rounds):
            print_to_console("rounds",str(i))
            if not i:
                content=THOUGHT_AND_ACTION.format(
                    tools=dumps(tools_desc),
                    question=user_input,
                    history=history,
                )
                messages=[{"role":"user","content":content}]

            response:str=(self.llm_client.call(messages,temperature=0.5))# type: ignore [args-type]
            print_to_console("raw_plan&solve_back",response)
            history+=response

            if isinstance(json.loads(response),list):
                print_to_console("result",response[1])
                break
            response_content:dict=json.loads(response)
            think:str=response_content["think"]
            print_to_console("think",think)
            action:str=response_content["action"]
            print_to_console("action",action)
            parameter:str=response_content["parameter"]
            print_to_console("parameter",parameter)

            print_to_console("action",action)
            print_to_console("keys",str(tool_register.tools.keys()))
            if  action in tool_register.tools.keys():
                print("parameter的参数里面:"+parameter)
                query:str=json.loads(parameter)["query"]
                func:Callable=tool_register.tools[action]["func"]
                search_response:SearchResponse=func(query)
                search_result:dict={
                    "content":search_response.result,
                    "answer":search_response.answer
                }
                observe_response:str=self.observation.observe(dumps(search_result))
                print_to_console("observation",json.loads(observe_response)["observation"])
                history+=observe_response
                print_to_console("history_in_round_end",str(history))
                
def print_to_console(tag:str,content:str)->None:
    print(f"[{tag}]:{content}"+"\n",flush=True)


                
