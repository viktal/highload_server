import os
import mimetypes
from urllib.parse import urlparse
from models import Request, Response
import config

REQUEST_METHODS = ['GET', 'HEAD']


def handler(request_data):
    # request
    request = Request(request_data.decode('utf-8'))

    # file path
    path = config.ROOT_DIR + urlparse(request.url).path
    if request.url.endswith("/"):
        path += "index.html"
    path_is_exist = os.path.exists(path)

    # response
    if request.method not in REQUEST_METHODS:
        response = Response(method=request.method, protocol=request.protocol, status=405)

    elif "/.." in request.url or (request.url.endswith("/") and not path_is_exist):
        if mimetypes.guess_type(request.url[:-1])[0] is None:
            response = Response(method=request.method, protocol=request.protocol, status=403)
        else:
            response = Response(method=request.method, protocol=request.protocol, status=404)

    elif (not request.is_valid) or (not path_is_exist):
        response = Response(method=request.method, protocol=request.protocol, status=404)
    else:
        content_type = mimetypes.guess_type(path)[0]
        with open(path, 'rb') as stream:
            data = stream.read()
        if len(data) == 0:
            print(path, content_type, data, len(data))
        response = Response(method=request.method, protocol=request.protocol, status=200,
                            content_type=content_type, content_length=len(data))

    headers = response.get_headers()
    if request.method == 'GET' and response.status == 200:
        return [headers, data]
    else:
        return [headers]
