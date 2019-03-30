import asyncio
import websockets
import time

async def handler(websocket, path):
    query = await websocket.recv()
    print(query)
    response = f"{round(time.time() * 1000)}"
    await websocket.send(response)
    print("complete")

start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

