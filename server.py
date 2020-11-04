import datetime
import email
import io
import json
import os
import pprint

from gevent import socket
import sys

"""
inspired by:
* https://ruslanspivak.com/lsbaws-part2/
* PEP3333
* http://blog.pythonisito.com/2012/07/introduction-to-gevent.html
* https://itnext.io/build-gunicorn-from-scratch-d75870960b9b
* https://docs.python.org/3/library/wsgiref.html#wsgiref.simple_server.WSGIServer
"""

class Server(object):
    def __init__(self, server_address):
        self._socket, self._server_name, self._port = self.__init_socket(server_address)
        self._headers = None
        self._status = None
        self._app = None
        self._path = None
        self._request_version = None
        self._request_data = None
        self._request_method = None

    def __init_socket(self, server_address):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPV4 and TCP
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # enables reusing the socket
        server_socket.bind(server_address)
        server_socket.listen(5) # standard queue size
        host, port = server_socket.getsockname()[:2]
        server_name = socket.getfqdn(host)
        return server_socket, server_name, port

    def get_environ(self):
        environ = {}
        environ['SERVER_NAME'] = self._server_name
        environ['REQUEST_METHOD'] = self._request_method
        environ['PATH_INFO'] = self._path
        environ['SERVER_PORT'] = str(self._port)
        environ['wsgi.url_scheme'] = 'http'
        environ['wsgi.input'] = io.StringIO(self._request_data) # creates a string stream
        environ['wsgi.errors'] = sys.stderr
        environ['wsgi.multithread'] = False # greenlets how will this work?
        environ['wsgi.multiprocess'] = False # too expensive
        environ['wsgi.run_once'] = False
        environ['wsgi.version'] = (1, 0)
        return environ

    def start_response(self, status, response_headers, exc_info=None):
        response = dict((x, y) for x, y in response_headers)
        response['Date'] = datetime.datetime.utcnow().date()
        response['Server'] = 'Server 1.0'
        #print(response)
        self._headers = response
        self._status = status

    def set_app(self, app):
        self._app = app

    def serve_forever(self):
        while True: # <-- this is not good
            # get connection and address
            client_connection, _ = self._socket.accept()
            self.handle_request(client_connection)

    def handle_request(self, client_connection):
        data = client_connection.recv(1024)
        try:
            parsed_request = self.parse_req(data.decode('utf-8'))
            self._request_method, self._path, self._request_version = parsed_request
        except Exception as e:
            print(e)
            sys.exit(1)
        app_result = self._app(self.get_environ(), self.start_response)
        self.send_response(app_result, client_connection)

    def parse_req(self, request):
        result = request.split()[:3]
        if isinstance(result, tuple)
            return result
        return Exception("Incorrect http request line")

    def make_response(self, app_result):
        status, response_headers = self._status, self._headers
        response = f'HTTP/1.1 {status}{os.linesep}'
        for header in response_headers.items():
            key, val = header
            response = response + f'{key}: {val}{os.linesep}'
        response = response + os.linesep
        for item in app_result:
            response = response + item.decode('utf-8')
        return response

    def send_response(self, app_result, client_connection):
        try:
            response = self.make_response(app_result)
            print(response)
            response_bytes = response.encode()
            client_connection.sendall(response_bytes)
        except Exception as e:
            print(e)
        client_connection.close()