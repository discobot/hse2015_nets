import asyncio
from aiohttp import web

loop = asyncio.get_event_loop()

app = web.Application(loop=loop)
messages = []

async def get_messages(request):
    return web.json_response(messages)

async def post_message(request):
    messages.append(dict(await request.post()))
    return web.Response()

app.router.add_route("GET", "/", get_messages)
app.router.add_route("POST", "/", post_message)

async def init(loop):
    server = await loop.create_server(app.make_handler(),
                                      "127.0.0.1", 8888)
    return server

if __name__ == "__main__":
    loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

