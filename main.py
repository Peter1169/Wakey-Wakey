import os
import uvicorn
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from threading import Thread

# Time (in seconds)
TIME_INTERVAL = 120 # Interval to make a GET request to an URL
ERROR_WAIT_TIME = 300 # Interval to make a GET request to an URL after a failed response

FILE_NAME = "wake-up.txt"
SELF_URL = "http://127.0.0.1:8000"

app = FastAPI()


class URL(BaseModel):
    url: str


@app.head("/")
@app.get("/")
async def root():
    return {"message": "WAKE UP SLEEPY HEAD!"}


async def fetch_url(url: str):
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
            response.raise_for_status()
            json_response = response.json()
            print(f"Response from {url}: {json_response}")
            await asyncio.sleep(TIME_INTERVAL)
        except (httpx.HTTPStatusError, ValueError):
            print(f"Error or invalid JSON from: {url}")
            await asyncio.sleep(ERROR_WAIT_TIME)


async def url_loop():
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            f.write(SELF_URL + "\n")

    with open(FILE_NAME, "r") as f:
        urls = f.readlines()

    tasks = [asyncio.create_task(fetch_url(url.strip())) for url in urls]
    for task in tasks:
        await task


@app.on_event("startup")
async def startup_event():
    await asyncio.sleep(1)
    asyncio.create_task(url_loop())


def run() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    print("GOODMORNING!!!!")
    thread = Thread(target=run)
    thread.start()