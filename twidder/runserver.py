from gevent.pywsgi import WSGIServer
from server import app

from geventwebsocket.handler import WebSocketHandler

import os

port = int(os.environ.get("PORT", 5000))

http_server = WSGIServer(('', port), app, handler_class=WebSocketHandler)
http_server.serve_forever()