import os
import uvicorn
import asyncio
from fastapi import FastAPI
import aiohttp
from threading import Thread

# Time (in seconds)
TIME_INTERVAL = 120 # Interval to make a GET request to an URL
ERROR_WAIT_TIME = 300 # Interval to make a GET request to an URL after a failed response

FILE_NAME = "wake-up.txt"
SELF_URL = "http://127.0.0.1:8000"

app = FastAPI()

@app.head("/")
@app.get("/")
async def root():
    return {"message": "WAKE UP SLEEPY HEAD!"}

async def fetch_url(url: str):
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    json_response = await response.json()
            print(f"Response from {url}: {json_response}")
            await asyncio.sleep(TIME_INTERVAL)
        except (aiohttp.ClientResponseError, ValueError):
            print(f"Error or invalid JSON from: {url}")
            await asyncio.sleep(ERROR_WAIT_TIME)

async def url_loop():
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            f.write(SELF_URL + "\n")

    with open(FILE_NAME, "r") as f:
        urls = f.readlines()

    tasks = [asyncio.create_task(fetch_url(url.strip())) for url in urls]
    await asyncio.gather(*tasks)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(url_loop())

def run() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)

def keep_loop_running(loop):
    asyncio.set_event_loop(loop)
    while True:
        loop.run_forever()

if __name__ == "__main__":
    print("GOODMORNING!!!!")
    loop = asyncio.new_event_loop()
    t1 = Thread(target=run)
    t2 = Thread(target=keep_loop_running, args=(loop,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()