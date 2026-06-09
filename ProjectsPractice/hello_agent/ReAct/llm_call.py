from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import Iterator

env=("API_KEY","BASE_URL","MODEL_ID")

def env_loader(name:str)->str:
    from os import getenv
    val=getenv(name)
    if val is None:
        raise EnvironmentError(f"检查您在.env的环境变量配置{name}")
    return val

[API_KEY,BASE_URL,MODEL_ID]=[env_loader(x) for x in env]

class LLMCall :
    def __init__(self) -> None:
        self.client:OpenAI=OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )
    def call_in_stream(self,messages:list[ChatCompletionMessageParam],temperature:float=0.7)->Iterator[str]:
        try:
            response=self.client.chat.completions.create(
                messages=messages,
                model=MODEL_ID,
                stream=True,
                temperature=temperature
            )
         
            print("模型响应成功！")b
            for chunk in response:
                if not chunk.choices:
                    continue
                content=chunk.choices[0].delta.content or ""
                yield content

        except Exception as e:
            raise RuntimeError("模型请求错误")from e
    def call(self,messages:list[ChatCompletionMessageParam],temperature:float=0.7)->str:
        try:
            response=self.client.chat.completions.create(
                messages=messages,
                model=MODEL_ID,
                stream=False,
                temperature=temperature
            )
         
            print("模型响应成功！")
            content=response.choices[0].message.content or ""
            return content
        except Exception as e:
            raise RuntimeError("模型请求错误")from e
