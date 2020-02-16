import asyncio
import websockets
import json
import random
import time

async def handler(websocket: websockets.server.WebSocketServer, path: str) -> None:
    motors = [0] * 4
    while True:
        result = await websocket.recv()
        result = json.loads(result)
        print(result)

        motors[0] += result['pitch'] # clockwise front front
        motors[2] -= result['pitch']
        motors[1] += result['roll']
        motors[3] -= result['roll']
        for i in range(len(motors)): 
            motors[i] += result['throttle']
            motors[i] = max(0, min(100, motors[i]))
        
        await websocket.send(json.dumps({
            "time": int(round(time.time() * 1000)),
            "orientation": {},
            "state": {
                "motors": motors
            }
        }))


start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
