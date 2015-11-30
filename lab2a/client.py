import sys
import asyncio
import aiohttp

SERVER_URL="http://localhost:8888"

async def post_message(text):
    async with aiohttp.post(SERVER_URL, data={"text": text}) as req:
        pass

async def get_messages():
    async with aiohttp.get(SERVER_URL) as response:
        return await response.json()

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    if sys.argv[1] == "get":
        print(loop.run_until_complete(get_messages()))
    elif sys.argv[1] == "post":
        loop.run_until_complete(post_message(sys.argv[2]))
