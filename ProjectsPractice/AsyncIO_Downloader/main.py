import asyncio
import logging
import sys
from random import randint
from typing import AsyncGenerator

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)-7s] [%(filename)-14s:%(lineno)-4d] %(message)s",
    level=logging.INFO,
    stream=sys.stderr,
)
log=logging.getLogger()

async def fake_download(name:str):
    time=randint(6,10)
    await asyncio.sleep(time)
    print(f"{name}完成，经历{time}秒")
    ...

class Measurer:
    def __await__(self):
        yield



async def download_manager(urls:list[str],max_concurrent:int):
    tasks=[]

    for x in urls:
        log.info(f"当前是{x}")

        while True:
            loop=asyncio.get_running_loop()
            all_tasks=asyncio.all_tasks(loop)
            if len(all_tasks)<max_concurrent:
                tasks.append(asyncio.create_task(fake_download(x)))
                log.debug(f"{x}appened")
                await asyncio.sleep(0)
                log.debug(str(len(all_tasks))+"=========================")
                break
            else:
                await Measurer()
    # print(*all_tasks,sep="\n\n")
    await asyncio.gather(*tasks)

    ...


async def main():
    urls=["url1","url2","url3","url4","url5"]
    await download_manager(urls,max_concurrent=3)
    log.debug("main")

asyncio.run(main())
