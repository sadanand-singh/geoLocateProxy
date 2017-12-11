"""
    ProxyRequestHandler
    ~~~~~~~~~~~~~~~~~~~

    HTTP Request Handler for our geoCode proxy server.

"""

import json
from collections import OrderedDict
from functools import partial
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from geoCoder import GeoCoder

class LimitedSizeDict(OrderedDict):
    """Dict with fixed size"""

    def __init__(self, *args, **kwargs):
        self.size_limit = kwargs.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwargs)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.size_limit is not None:
            while len(self) > self.size_limit:
                # Pop items in FIFO order
                self.popitem(last=False)


class memoize(object):
    """cache the return value of a method

    This class is meant to be used as a decorator of methods. The
    return value
    from a given method invocation will be cached on the instance
    whose method was invoked.All arguments passed to a method
    decorated with memoize must be hashable.

    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return partial(self, obj)

    def __call__(self, *args, **kw):
        obj = args[0]
        try:
            cache = obj.cache
        except AttributeError:
            cache = obj.cache = LimitedSizeDict(size_limit=100)

        key = args[1]
        try:
            res = cache[key]
        except KeyError:
            res = cache[key] = self.func(*args, **kw)

        status, coords = res
        return status, coords

class ProxyRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request handler component for the proxy server.

    It performs the do_GET operations for our proxy server. Uses helper
    classes :py:class:`GeoCoder <geoCoder>` to make requests to
    external service providers.
    """

    msgs = {}
    msgs[400] = 'Please provide an address to geocode your request query string (e.g. "?address=PostMates Office, CA")'
    msgs[503] = 'There are no geocoding services available. Try again later.'
    msgs[404] = 'Adrress did not found on any providers!'

    def do_GET(self):
        """ perform the GET call to the proxy server. """

        status, coords = self.__geocoding()

        if status >= 400:
            if status in [400, 404, 503]:
                self.__send_json(status, {'message': self.msgs[status]})
            else:
                msg = "Can not process this request. Status: {0}"
                self.__send_json(status, {'message': msg.format(status)})
            return

        msg = {"Latitude": coords[0], "Longitude": coords[1]}
        self.__send_json(status, msg)
        return

    def __geocoding(self):
        """ Helper method to create geoCoder instance and call providers

        Args:
            None

        Returns:
            status, coords: Response status code and list of coords

        """

        geocoder = GeoCoder()
        uri = urlparse(self.path)
        query = parse_qs(uri.query)
        status = 400

        if query.get('address') is None:
            return status, None

        status, coords = geocoder.get_geocode(query['address'][0])

        return status, coords

    def __send_json(self, http_status_code, data):
        """Helper method to send json data to server

        Args:
            http_status_code: HTTP status code response from external API
            data: relevant message for decoding the status, or coordinates

        """

        text = json.dumps(data)
        self.send_response(http_status_code)
        self.end_headers()
        self.wfile.write(text.encode('utf-8'))

        return
