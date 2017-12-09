"""
    GeoCoder
    ~~~~~~~~~

    The geoCoding component for the geoCode Proxy server.

"""

class GeoCoder:
    """A GeoCoder is the agent to query set of external service providers.

    It sets up all external service providers based on the `config.json`
    file and aids
    :py:class:`ProxyRequestHandler <geoCoder.proxyRequestHandler>`
    to retrieve coordinates from the appropriate external provider.
    Each external provider is an instance of
    :py:class:`ExternalServiceProvider <geoCoder.externalServiceProvider>`.
    """

    def __init__(self, primaryService):
        """Geocoder Initializer

        Setups primary service definition and all other services based
        on user defined json files.

        Args:
            primaryService: Name of the primary service provider

        """

        self.primaryService = primaryService
        self.services = []
        self.setupServiceProviders()


    def setupServiceProviders(self):
        """Create all instances of external service providers based on user defined services.json file """

        # Read the services.json file to get all providers

        # check if primaryService exists in this data

        # load corresponding secrets from services.secrets.json

        # create ExternalServiceProvider objects
        return


    def getGeoCode(self, address):
        """ get cords from external service for a given address"""

        return results
