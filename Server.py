import socket
import config
import logging
from Worker import Worker


class Server:
    def __init__(self):
        self.server_address = config.SERVER_ADDRESS

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        logging.basicConfig(level=logging.INFO)
        logging.info(f'Server start on {config.SERVER_ADDRESS}')
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
