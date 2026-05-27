
from llm_call import LLMCall

EXECUTOR_SYSTEM_PROMPT="""
你需要按照计划执行既定的plan
# PLAN
{plan}
# HISTORY
{history}
# task
{task}
# Attention
你的输出需要直接输出本轮做了什么，完成了plan的第几步
# format
[第N步完成,做了什么]
"""

class Executor:
    def __init__(self,client:LLMCall)->None:
        self.client=client
    def execute(self,plan:list[str])->None:
        for x in plan:
            history=[]
            try:
                content=EXECUTOR_SYSTEM_PROMPT.format(
                plan=str(plan),
                history=str(history),
                task=str(x)
            )
            except Exception as e:
                raise ValueError("检查您传入的格式") from e
            messages=[{"role":"user","content":content}]
            print(
                "当前模型的执行进度是：")
            item=""
            for x in self.client.call(messages):# type: ignore[arg-type]
                print(x,end="",flush=True)
                item+=x
            history.append(x)