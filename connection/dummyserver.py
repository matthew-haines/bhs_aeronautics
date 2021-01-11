import asyncio
import json
import time
import websockets
import numpy as np

def rotation_quaternion(euler):
    # q = [x, y, z, w]
    s = np.sin 
    c = np.cos
    r = euler[0]
    p = euler[1]
    y = euler[2]
    return [
        s(r)*c(p)*c(y)-c(r)*s(p)*s(y),
        c(r)*s(p)*c(y)+s(r)*c(p)*s(y),
        c(r)*c(p)*s(y)-s(r)*s(p)*c(y),
        c(r)*c(p)*c(y)+s(r)*s(p)*s(y)
    ]

async def handler(websocket: websockets.server.WebSocketServer, path: str) -> None:
    motors = [0] * 4
    j = 0
    while True:
        result = await websocket.recv()
        result = json.loads(result)

        motors[0] += result['pitch'] # clockwise front front
        motors[2] -= result['pitch']
        motors[1] += result['roll']
        motors[3] -= result['roll']
        for i in range(len(motors)): 
            motors[i] += result['throttle']
            motors[i] = max(0, min(100, motors[i]))
        
        await websocket.send(json.dumps({
            "time": int(round(time.time() * 1000)),
            "orientation": rotation_quaternion([j/300, j/150, j/200]),
            "motors": motors
        }))
        j += 1


start_server = websockets.serve(handler, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
