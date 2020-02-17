import asyncio
import websockets

async def test():
    url = 'ws://192.168.4.1:5678'
    async with websockets.connect(url) as websocket:
        while True:
            result = await websocket.recv()
            print(result)

asyncio.get_event_loop().run_until_complete(test())
