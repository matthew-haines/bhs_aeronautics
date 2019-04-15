import asyncio
import websockets
import time
import json
import threading


def get_current_time():
    return int(round(time.time() * 1000))


class Server:

    def __init__(self, port: int = 8765, host: str = 'localhost', timeout_time: float = 100):
        """
        Complete Websocket server and response handler.

        Parameters:
        port: The port that the server listens on

        host: the hostname of the server

        timeout_time: Maximum amount of time in milliseconds that the server will wait after each message
            for the next message before initiating a safety shutdown procedure for the quadcopter.


        """
        # General
        self.timeout_time = timeout_time

        # Actual controller (change)
        self.controller = None

        # Start Websockets Server
        self.last_command = None
        asyncio.run(self.__serve(port, host))

    def __timeout_check(self):
        while (1):
            if get_current_time() - self.last_command > self.timeout_time:
                print('timed out')
                self.controller.abort_sequence()
                self.timeout_check.join()

    async def __handler(self, websocket: websockets.server.WebSocketServer, path: str):
        while (1):
            command = await websocket.recv()
            if self.last_command == None:
                self.last_command = get_current_time()
                self.timeout_check = threading.Thread(target=self.__timeout_check)
                self.timeout_check.start()

            print(command)
            self.last_command = get_current_time()
            # parsed = json.loads(command)

    async def __serve(self, port: int, host: str):
        server = await websockets.serve(self.__handler, host, port)
        await server.wait_closed()


server = Server()