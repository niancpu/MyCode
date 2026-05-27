from executor import Executor
from planner import Planner
from llm_call import LLMCall

def main():

    client = LLMCall()

    user_input="一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
    print(f"问题：{user_input}")
    executor=Executor(client)
    planner=Planner(client) 
    plan=planner.plan(user_input)
    executor.execute(plan)



if __name__ == "__main__":
    main()
