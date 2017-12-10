"""
    GeoCoder
    ~~~~~~~~~

    The geoCoding component for the geoCode Proxy server.

"""

import json
from geoCoder.externalServiceProvider import ExternalServiceProvider


class GeoCoder:
    """A GeoCoder is the agent to query set of external service providers.

    It sets up all external service providers based on the `config.json`
    file and aids
    :py:class:`ProxyRequestHandler <geoCoder.proxyRequestHandler>`
    to retrieve coordinates from the appropriate external provider.
    Each external provider is an instance of
    :py:class:`ExternalServiceProvider <geoCoder.externalServiceProvider>`.
    """

    def __init__(self, primary):
        """Geocoder Initializer

        Setups primary service definition and all other services based
        on user defined json files.

        Args:
            primary: Name of the primary service provider

        """

        self.primary_service = primary
        self.services = []
        self.num_services = 0
        self.setup_service_providers()


    def setup_service_providers(self):
        """Create all instances of external service providers based on user defined services.json

        Args:
            None

        """

        # Read the services.json file to get all providers
        config = {}
        with open("./services.json", "r") as cfile:
            config = json.loads(cfile.read())

        # check if primaryService exists in this data
        providers = []
        if self.primary_service in config.keys():
            providers.append(self.primary_service)
        else:
            msg = "Requested Primary Service {0} is not defined in the services.json file"
            raise ValueError(msg.format(self.primary_service))

        secondary = [x for x in config.keys() if x != self.primary_service]
        providers += secondary

        # load corresponding secrets from services.secrets.json
        secrets = {}
        with open("./services.secrets.json", "r") as sfile:
            secrets = json.loads(sfile.read())
            missing = list(set(providers) - set(list(secrets.keys())))
            if missing:
                msg = "Secrets not provided for services: {0}!"
                raise ValueError(msg.format(missing))

        # create ExternalServiceProvider objects
        for serv in providers:
            service_config = config[serv]
            service_config["name"] = serv
            sconf = secrets[serv]
            service_config["api_key_params"] = sconf["api_key_params"]
            self.services.append(ExternalServiceProvider(service_config))

        # update total no. of services
        self.num_services = len(self.services)

    def getGeoCode(self, address):
        """ get cords from external service for a given address"""

        return results
