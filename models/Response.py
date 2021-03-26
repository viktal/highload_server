from datetime import datetime

STATUS_MESSAGES = {
    200: 'OK',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
}


class Response:
    def __init__(self, method, protocol, status, content_type=None, content_length=0):
        self.method = method
        self.protocol = protocol
        self.status = status
        self.content_type = content_type
        self.content_length = content_length

        self.server = 'talmaza`s'
        self.date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.connection = 'close'

    def get_headers(self):
        headers = f'{self.protocol} {self.status} {STATUS_MESSAGES[self.status]}\r\n' \
                  f'Server: {self.server}\r\n' \
                  f'Date: {self.date}\r\n'

        if self.content_type:
            headers += f'Content-Type: {self.content_type}\r\n'

        headers += f'Content-Length: {self.content_length}\r\n' \
                   f'Connection: {self.connection}\r\n\r\n'

        return headers.encode()
