import sys
from server import Server
from urllib.request import urlopen
import json

def make_server(server_address, application):
    server = Server(server_address, 2000)
    server.set_app(application)
    return server

def main():
    module = __import__("flaskapp")
    application = getattr(module, "app")
    host = ''
    port = 80
    server = make_server((host, port), application)
    server.serve_forever()

if __name__ == '__main__':
    main()
