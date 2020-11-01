import io
from gevent import socket
import sys


class Server(object):
    def __init__(self):
        self.address_family = socket.AF_INET #IPV4
        self.socket_type = socket.SOCK_STREAM # TCP
        self.request_queue_size = 5 # standard queue size
        self._app = None

    def set_app(self, app):
        self._app = app

    def get_environ(self):
        return NotImplementedError()

    def start_response(self):
        return NotImplementedError()

