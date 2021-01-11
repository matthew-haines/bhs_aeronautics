import asyncio
import json
import time
import websockets
import numpy as np
from env import Simulation

async def handler(websocket: websockets.server.WebSocketServer, path: str) -> None:
    sim = Simulation()
    motors = [0] * 4
    j = 0
    throttle = 0
    while True:
        result = await websocket.recv()
        result = json.loads(result)
        throttle += result['throttle']

        motors[0] = (1 + 0.1 * result['pitch']) * throttle # clockwise front front
        motors[2] = (1 - 0.1 * result['pitch']) * throttle
        motors[1] = (1 + 0.1 * result['roll']) * throttle
        motors[3] = (1 - 0.1 * result['roll']) * throttle

        for i in range(len(motors)): 
            motors[i] = 10 * max(0, min(100, motors[i]))
        
        # 10 ms interaction loop
        for _ in range(int(round(0.01 / sim.dt))):
            sim.step(motors)

        motors = list(map(lambda x: x / 10, motors))

        await websocket.send(json.dumps({
            "time": int(round(time.time() * 1000)),
            "orientation": list(sim.rotation_quaternion()),
            "motors": motors
        }))
        j += 1


start_server = websockets.serve(handler, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()