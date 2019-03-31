import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
import datetime
import requests
import threading


async def make_requests(urls):
    print("start_time: {0}".format(datetime.datetime.now()))
    print("Current Thread: ({0})".format(threading.currentThread()))
    executor = ThreadPoolExecutor(max_workers=10)
    futures = [loop.run_in_executor(executor, requests.get, uri) for uri in urls]
    responses = await asyncio.gather(*futures)

    return responses


if __name__ == "__main__":
    main_start_time = time.time()
    print("start_time: {0}".format(datetime.datetime.now()))
    print("Main Thread Start: ({0})".format(threading.currentThread()))

    print("\n----------------- async start -----------------")
    urls_set = ["https://www.baidu.com", "https://www.qq.com"] * 100
    loop = asyncio.get_event_loop()
    rsp = loop.run_until_complete(make_requests(urls_set))

    # print(rsp[1].text)
    async_spend_time = time.time()
    print("asyncio spend time: {0}".format(async_spend_time - main_start_time))
    print("\n----------------- async stop -----------------")

    start = time.time()
    for url in urls_set:
        requests.get(url)

    print("single spend time: {0}".format(time.time() - async_spend_time))
