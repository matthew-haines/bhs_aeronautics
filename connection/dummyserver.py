import asyncio
import websockets
import json
import random

async def handler(websocket: websockets.server.WebSocketServer, path: str) -> None:
    while True:
        result = await websocket.recv()
        result = json.loads(result)
        print(result)
        await websocket.send(json.dumps({
            "state": {
                "motors": [
                    random.randint(0, 100),
                    random.randint(0, 100),
                    random.randint(0, 100),
                    random.randint(0, 100)
                ]
            }
        }))


start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

