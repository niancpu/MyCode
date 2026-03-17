from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY=os.getenv("SF_API_KEY")
BASE_URL= "https://api.siliconflow.cn/v1"

client=OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL

)

response=client.chat.completions.create(
    model="model",
    messages=[
        {"role":"system","content":"你是凑企鹅"},  
        {"role":"user","content":"user_input"}
    ],
    temperature=0.5,
    max_tokens=200000
)

reply=response.choices[0].message.content

