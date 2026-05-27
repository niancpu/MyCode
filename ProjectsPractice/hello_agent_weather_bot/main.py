import re
import os
from tavily import TavilyClient
import tools
from openai import OpenAI
import system_prompt
from dotenv import load_dotenv


def main():
    print("Hello from hello-agent!")

def get_env(name:str)->str:#通过一个get_env函数批量获取环境变量同时进行类型检验
    val = os.getenv(name)
    if val is None:
        raise ValueError(f"缺少环境变量：{name}")
    return val

# --- 2. 初始化 ---
load_dotenv()

TAVILY_API_KEY,BASE_URL,API_KEY,MODEL_ID=[get_env(k) for k in ("TAVILY_API_KEY","BASE_URL","API_KEY","MODEL_ID")]

llm = OpenAI(

    api_key=API_KEY,
    base_url=BASE_URL
)

user_prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"
prompt_history = [f"用户请求: {user_prompt}"]

print(f"用户输入: {user_prompt}\n" + "="*40)

# --- 3. 运行主循环 ---
for i in range(5): # 设置最大循环次数
    print(f"--- 循环 {i+1} ---\n")
    
    # 3.1. 构建Prompt
    full_prompt = "\n".join(prompt_history)
    
    # 3.2. 调用LLM进行思考
    response=llm.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role":"user","content":user_prompt},
            {"role":"system","content":system_prompt.AGENT_SYSTEM_PROMPT}
        ]
    )

    llm_output=response.choices[0].message.content or ""

    # 模型可能会输出多余的Thought-Action，需要截断
    match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
    if match:
        truncated = match.group(1).strip()
        if truncated != llm_output.strip():
            llm_output = truncated
            print("已截断多余的 Thought-Action 对")
    print(f"模型输出:\n{llm_output}\n")
    prompt_history.append(llm_output)
    
    # 3.3. 解析并执行行动
    action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
    if not action_match:
        observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)
        continue
    action_str = action_match.group(1).strip()

    if action_str.startswith("Finish"):
        if final_match := re.match(r"Finish\[(.*)\]", action_str):
            final_answer=final_match.group(1)
        print(f"任务完成，最终答案: {final_answer}")
        break
    
    if(tool_match := re.search(r"(\w+)\(", action_str)):
        tool_name = tool_match.group(1)
    if(args_str_match := re.search(r"\((.*)\)", action_str)):
        args_str=args_str_match.group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

    if tool_name in tools.available_tools:
        observation = tools.available_tools[tool_name](**kwargs)
    else:
        observation = f"错误:未定义的工具 '{tool_name}'"

    # 3.4. 记录观察结果
    observation_str = f"Observation: {observation}"
    print(f"{observation_str}\n" + "="*40)
    prompt_history.append(observation_str)


if __name__ == "__main__":
    main()
