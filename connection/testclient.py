import asyncio
import websockets
import time

async def query():
    async with websockets.connect(
        'ws://localhost:8765') as websocket:
            for i in range(50):
                await websocket.send("ping")
                time.sleep(0.05)


asyncio.get_event_loop().run_until_complete(query())

