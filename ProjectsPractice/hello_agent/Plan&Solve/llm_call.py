from dotenv import load_dotenv
load_dotenv()
from typing import Iterator
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
env=("API_KEY","BASE_URL","MODEL_ID","TAVILY_API_KEY")

def env_loader(name:str):
    from os import getenv
    val=getenv(name)
    if val is None:
        raise EnvironmentError("检查您在.env的环境变量配置")
    return val

[API_KEY,BASE_URL,MODEL_ID,TAVILY_API_KEY]=[env_loader(x) for x in env]

class LLMCall :
    def __init__(self) -> None:
        self.client:OpenAI=OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )
    def call(self,messages:list[ChatCompletionMessageParam])->Iterator[str]:
        try:
            response=self.client.chat.completions.create(
                messages=messages,
                model=MODEL_ID,
                stream=True
            )
         
            print("模型响应成功！")
            collected_content=[]
            for chunk in response:
                if not chunk.choices:
                    continue
                content=chunk.choices[0].delta.content or ""
                collected_content.append(content)
                yield content

        except Exception as e:
            raise RuntimeError("模型请求错误")from e
        
