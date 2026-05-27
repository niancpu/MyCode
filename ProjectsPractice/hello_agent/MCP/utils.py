# from os import getenv
# from dotenv import load_dotenv,dotenv_values
# from typing import Generator
# load_dotenv()

# def load_env_all()->None:
#     env_dict=dotenv_values()
#     for key in env_dict.keys():
#         env_dict[key]=next(load_env(key))

# def load_env(*name:str)->Generator[str,None,None]:
    
#     for val in name:
#         env=getenv(val)
#         if env is None:
#             raise EnvironmentError(f"环境变量{name}获取失败")
#         yield env



