# WSGI_server
A WSGI server implemented with python and gevent.

###About
Do not use this server in production. Security is pretty much
nonexistent. Also see the Todo list before actually using this
server.

This is not a 100 % pure WSGI server implementation. There
are still a few things missing, but it's good enough to run
web frameworks like Flask or Django.

This implementation uses greenlets since they have I/O centric
scheduling. Python threads are limited by GIL, and processes
are usually expensive. But gevent greenlets yield automatically
when blocking I/O which makes them really good for networking.

###Performance
It's possible to get 400 requests per second using Flask. This
was measured using ApacheBench (https://httpd.apache.org/docs/2.4/programs/ab.html)

## Todo

* Signal handling (SIGINT for instance) for terminating the server.
* Greenlets do not join the server on termination (gevent.joinall)
* Implement 404 return on incorrect request. Currently if the client sends an incorrect
http request line then it will result in an exception on the server
* Return write on start_response. This is still not a pure WSGI server

##More information
This implementation was inspired by:
* https://ruslanspivak.com/lsbaws-part2/
* PEP3333
* http://blog.pythonisito.com/2012/07/introduction-to-gevent.html
* https://itnext.io/build-gunicorn-from-scratch-d75870960b9b
* https://docs.python.org/3/library/wsgiref.html#wsgiref.simple_server.WSGIServer