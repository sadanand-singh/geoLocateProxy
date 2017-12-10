#!/usr/bin/env python3

"""
    Script to start the GeoCode Proxy Server
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    It takes two optional parameters "--server" and "--port" to control
    the addres and port to run the server.

"""

from http.server import HTTPServer
from geoCoder.proxyRequestHandler import ProxyRequestHandler
from argparse import ArgumentParser
import sys

def serve(address, port, handler=ProxyRequestHandler):
    httpd = HTTPServer((address, port), handler)
    print("Server is running at http://{0}:{1}".format(address, port))
    httpd.serve_forever()

    return

if __name__ == "__main__":

    parser = ArgumentParser(description="Run GeoCode Proxy Server")

    msg = "Server Address (default='0.0.0.0')"
    parser.add_argument("-s", "--server", default='0.0.0.0', help=msg)

    msg = 'Server Port (default=8088)'
    parser.add_argument("-p", "--port", default=8088, type=int, help=msg)

    args = parser.parse_args()

    try:
        serve(args.server, args.port)
    except KeyboardInterrupt:
        print("\nProgram Interrupted, Exiting!")
        sys.exit()
