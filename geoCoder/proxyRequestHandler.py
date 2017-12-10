"""
    ProxyRequestHandler
    ~~~~~~~~~~~~~~~~~~~

    HTTP Request Handler for our geoCode proxy server.

"""

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from geoCoder import GeoCoder


class ProxyRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request handler component for the proxy server.

    It performs the do_GET operations for our proxy server. Uses helper
    classes :py:class:`GeoCoder <geoCoder>` to make requests to
    external service providers.
    """

    messages = {}
    messages[400] = 'Please provide an address to geocode your request query string (e.g. "?address=PostMates Office, CA")'
    messages[503] = 'There are no geocoding services available. Try again later.'
    messages[404] = 'Adrress did not found on any providers!'


    def do_GET(self):
