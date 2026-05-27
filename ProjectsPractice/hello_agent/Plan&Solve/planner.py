import re
from llm_call import LLMCall
import json

PLANNER_SYSTEM_PROMPT="""
# Role
你是一名任务规划师，你需要将用户的问题的解决方案分解成简单的几个可执行的步骤，并且生成可实现的详细计划。
# Format of answer
```python
["步骤一，具体内容","步骤二，具体内容"..."步骤N，具体内容"]
```
# Attention
- "```python"和"```"是必要的
- 不要输出多余的废话
- **不要**输出结果，你只负责**计划和拆解任务**，比如：
```
## 反例（不要这样）：

```
**用户问题：**{question}
"""
class Planner:
    def __init__(self,client:LLMCall)->None:
        self.client=client

    def plan(self,user_input:str)->list[str]:
        content=PLANNER_SYSTEM_PROMPT.format(question=user_input)
        messages=[{"role":"user","content":content}]
        response=""
        
        print("模型的规划是：")

        for x in self.client.call(messages) :# type: ignore[arg-type]
            print(x,flush=True,end="")
            response+=x

        plan=json.loads(extract_between(response,"```python","```")[0])
        print("plan的项数为：", len(plan))
        return plan
    
def extract_between(text: str, start: str, end: str) -> list[str]:
    try:
        return re.findall(f"{re.escape(start)}(.*?){re.escape(end)}", text, re.DOTALL)
    except Exception as e:
        print(f"[warning] 提取失败：{e}")
        return []
           
        

