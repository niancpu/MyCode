from llm_call import LLMCall

OBSERVAE_PROMPT="""
你需要对于工具的回答做出来includsion和insight
# HISTORY
{history}
# OUTPUT FORMAT
`{
    "observation":"你的输出"
}`
"""

class Observation:
    def __init__(self) -> None:
        self.llm_client=LLMCall()
    
    def observe(self,results:str)->str:
        history=results
        content=OBSERVAE_PROMPT.format(history=history)
        messages=[{"role":"user","content":content}]
        print("=====正在Observe=====")
        response=self.llm_client.call(messages)# type: ignore [args-type]
        return response


