import socket
import config
from Worker import Worker


class Server:
    def __init__(self):
        self.server_address = config.SERVER_ADDRESS

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.socket.bind(config.SERVER_ADDRESS)
        self.socket.listen(500)
        self.socket.setblocking(False)

        processes = []
        for i in range(config.CPU):
            worker = Worker(self.socket)
            processes.append(worker)
            worker.start()

        for process in processes:
            process.join()
