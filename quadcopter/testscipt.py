import asyncio
import websockets
from imu import IMU

async def handler(websocket: websockets.server.WebSocketServerProtocol, path: str):
    imu = IMU()
    while True:
        await websocket.send(str(imu.sample()))
        await asyncio.sleep(0.5)

start_server = websockets.serve(handler, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
