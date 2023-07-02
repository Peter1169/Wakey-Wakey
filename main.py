import os
import uvicorn
import requests
from fastapi import FastAPI
from threading import Thread
from time import sleep

# Time (in seconds)
TIME_INTERVAL = 120  # Interval to make a GET request to an URL
ERROR_WAIT_TIME = 300  # Interval to make a GET request to an URL after a failed response

FILE_NAME = "wake-up.txt"
SELF_URL = "http://127.0.0.1:8000"

app = FastAPI()

@app.head("/")
@app.get("/")
async def root():
    return {"message": "WAKE UP SLEEPY HEAD!"}

def fetch_url(url: str):
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_response = response.json()
            print(f"Response from {url}: {json_response}")
            sleep(TIME_INTERVAL)
        except requests.exceptions.RequestException:
            print(f"Error from: {url}")
            sleep(ERROR_WAIT_TIME)

def url_loop():
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            f.write(SELF_URL + "\n")

    with open(FILE_NAME, "r") as f:
        urls = f.readlines()

    for url in urls:
        thread = Thread(target=fetch_url, args=(url.strip(),))
        thread.start()

def run() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    print("GOODMORNING!!!!")
    thread = Thread(target=run)
    thread.start()
    url_loop()
