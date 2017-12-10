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
        """ perform the GET call to the proxy server. """

        status, coords = self.__geocoding()

        if status >= 400:
            self.__send_json(status, {'message': self.messages[status]})
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
