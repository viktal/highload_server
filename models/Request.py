from urllib.parse import unquote


class Request:
    def __init__(self, request_data):
        self.method = ""
        self.url = ""
        self.protocol = ""
        self.is_valid = False

        try:
            (self.method, dirty_url, dirty_protocol) = request_data.split(" ")[0:3]
            self.protocol = dirty_protocol.split("\r")[0]
            self.url = unquote(dirty_url)
            self.is_valid = True
        except Exception:
            self.is_valid = False
