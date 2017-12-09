"""
    ProxyRequestHandler
    ~~~~~~~~~~~~~~~~~~~

    HTTP Request Handler for our geoCode proxy server.

"""

class ProxyRequestHandler:
    """HTTP Request handler component for the proxy server.

    It performs the do_GET operations for our proxy server. Uses helper
    classes :py:class:`GeoCoder <geoCoder>` to make requests to
    external service providers.
    """

    def do_GET(self):
