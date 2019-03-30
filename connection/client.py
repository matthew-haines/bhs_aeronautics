import asyncio
import websockets
import time

async def query():
    async with websockets.connect(
        'ws://flightcontroller:8765') as websocket:
        data = input()
        cur_time = int(round(time.time() * 1000))
        await websocket.send(data)
        response = await websocket.recv()
        time_diff = int(response) - cur_time
        print(f"Lag: {time_diff} ms")


while True:
    asyncio.get_event_loop().run_until_complete(query())

