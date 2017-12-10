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

    def __init__(self):
        """Geocoder Initializer

        Setups primary service definition and all other services based
        on user defined json files.

        Args:
            None

        """

        self.primary_service = ""
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

        # find Primary provider and curate a list of providers
        providers = self.__find_primary_provider(config)

        # throw an error if less than 2 providers have been provided
        if len(providers) < 2:
            msg = "At least 2 external providers are needed!"
            raise ValueError(msg)

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

    def __find_primary_provider(self, config):
        """ from the loaded json condif dict, find the primary provider.

        The primary provider is chosen based on the following logic:

        A. If a unique provider has "primary" key defined as "true" in
        the "services.json" file, it is promoted as "Primary" provider.

        B. If multiple providers have "primary" key defined as "true",
        randomly one of them is promoted as "Primary" provider.

        C. If none of the providers have "primary" key defined as
        "true", randomly one among all is promoted as "Primary"
        provider.

        Args:
            config: dict data from services.json

        Returns:
            providers: list of providers, first being primary

        """

        primary_providers = []
        providers = list(config.keys())

        for serv in providers:
            if "primary" in config[serv].keys():
                if config[serv]['primary'].lower() == "true":
                    primary_providers.append(serv)

        self.primary_service = providers[0]
        if primary_providers:
            self.primary_service = primary_providers[0]
            providers.remove(self.primary_service)
            providers = [self.primary_service] + providers

        return providers

    def get_geocode(self, address):
        """ get cords from external service for a given address.

        Args:
            address: address str for which coords are desired

        Returns:
            code, coords: Response code and list of coords

        """

        # Keep trying until Response is received
        count = 0
        status = 503
        coords = None
        while status >= 400 and count < self.num_services:
            geocode_service = self.services[count]
            print("Using Service: {0}...".format(geocode_service.name))
            # send request to the service
            status, coords = geocode_service.get_geocode(address)
            count += 1

        return status, coords
