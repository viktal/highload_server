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
    print(path)
    path_is_exist = os.path.exists(path)

    # response
    response: Response
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
        size = os.path.getsize(path)
        content_type = mimetypes.guess_type(path)[0]
        response = Response(method=request.method, protocol=request.protocol, status=200,
                            content_type=content_type, content_length=size)

    headers = response.get_headers()
    if request.method == 'GET' and response.status == 200:
        with open(path, 'rb') as stream:
            return [headers, stream.read()]
    else:
        return [headers]
