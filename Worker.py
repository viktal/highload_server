import multiprocessing
import asyncore
from handler import handler


class ClientHandler(asyncore.dispatcher):
    def __init__(self, socket, address):
        asyncore.dispatcher.__init__(self, socket)
        self.response = []
        self._readable = True

    def writable(self) -> bool:
        return bool(self.response)

    def readable(self) -> bool:
        return self._readable

    def handle_read(self) -> None:
        data = self.recv(1024)
        self.response.extend(handler(data))
        self._readable = False

    def handle_write(self) -> None:
        buffer = self.response[0]
        sent = self.send(buffer)
        if sent < len(buffer):
            self.response[0] = buffer[sent:]
        else:
            self.response.pop(0)
        if len(self.response) == 0:
            self.close()


class Dispatcher(asyncore.dispatcher):
    def handle_accept(self) -> None:
        client = self.accept()
        if client is not None:
            ClientHandler(*client)


class Worker(multiprocessing.Process):
    def __init__(self, socket):
        super(Worker, self).__init__()
        self.socket = socket

    def run(self):
        dispatcher = Dispatcher(self.socket)
        dispatcher.accepting = True
        asyncore.loop()
