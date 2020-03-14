import asyncio
import websockets
import json
import time
from imu import IMU

async def handler(websocket: websockets.server.WebSocketServer, path: str) -> None:
    imu = IMU() 
    while True:
        request = await websocket.recv()
        request = json.loads(request)
        data = imu.sample()
        await websocket.send(json.dumps({
            "time": int(round(time.time() * 1000)),
            "calibration": imu.check_calibration(),
            "orientation": data,
            "motors": [
                0, 0, 0, 0
            ]
        }))

start_server = websockets.serve(handler, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()