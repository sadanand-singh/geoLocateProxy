#!/usr/bin/env python3

"""
    Script to use/test the GeoCode proxy Service.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    It takes address as parameter and uses curl to make the request to
    the proxy server.

    The server and port are provided using two optional parameters
    --server and --port, same as the runproxy script.

"""

import subprocess
from argparse import ArgumentParser
from urllib.parse import quote
from urllib.request import urlopen
import sys
import os

if __name__ == "__main__":

    parser = ArgumentParser(description="Test GeoCode Proxy Server")

    msg = 'Address for which Geo Corrds are needed'
    parser.add_argument('address', help=msg)

    msg = "Server Address (default='localhost')"
    parser.add_argument("-s", "--server", default='localhost', help=msg)

    msg = 'Server Port (default=8088)'
    parser.add_argument("-p", "--port", default=8088, type=int, help=msg)


    args = parser.parse_args()

    server = args.server
    port = args.port
    address = quote(args.address)

    queryString = "http://{}:{}/?address={}".format(server, port, address)

    print("Running...")
    print("'curl {}'".format(queryString))

    try:
        subprocess.call(["curl", queryString])
    except OSError as err:
        if err.errno == os.errno.ENOENT:
            print("curl not Found! Please install before running.")
            print()
            print("Will test using urllib.requests.urlopen()...")
            fout = urlopen(queryString)
            print(fout.read().decode('UTF-8', 'ignore'))
        else:
            raise
    except KeyboardInterrupt:
        print("\nProgram Interrupted, Exiting!")
        sys.exit()
