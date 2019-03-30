from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import time

class Server(WebSocket):

    def handleMessage(self):
        self.sendMessage("{}".format(round(time.time() * 1000)))

    def handleConnected(self):
        print('connected')

    def handleClose(self):
        print('closed')


server = SimpleWebSocketServer('', 8765, Server)
server.serveforever()