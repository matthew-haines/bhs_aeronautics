import websockets
import asyncio
import json
import time

class websocket_server():

    def __init__(self, name='localhost', port=8765, heartbeat_interval=0.100):

        self.missed_heartbeats = 0
        self.last_heartbeat = 0

        self.server = websockets.serve(self.handler, name, port)
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def handler(self, websocket, path):
        message = await websocket.recv()

        if str(message) == 'ping':
            await websocket.send('pong')

        

    def json_parser(self, data):
        parsed = json.laods(data)
        # Do some stuff

        
