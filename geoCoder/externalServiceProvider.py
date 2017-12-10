"""
    ExternalServiceProvider
    ~~~~~~~~~~~~~~~~~~~~~~~~

    The external service provider component for the geoCode Proxy server.

"""

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError
import json


class ExternalServiceProvider:
    """An ExternalServiceProvider is the third party geoCode provider.

    It defines all properties of a third party service provider for the
    geoCode service. It also defines logic to parse the latitude and
    longitude of a given address appropriately. Behavior is completely
    controlled by the user defined configurations in `services.json`
    and `services.secrets.json` provided to initializer as a `dict`.
    """

    def __init__(self, serviceData):
        """ Sercvice Provider initializer

        Args:
            serviceData: A dict for with services info

        """

        self.name = serviceData["name"]
        self.base_url = serviceData["base_url"]
        self.query_address_string = serviceData["address_query_name"]
        self.coords_keys = serviceData["coord_obj_keys"]
        self.api_key_params = serviceData["api_key_params"]

    def get_coordinates(self, address):
        """ get coords from provider

        Args:
            address: address str for which coords are desired

        Returns:
            code, coords: Response code and list of coords

        """

        try:
            raw_data = self.__get_raw_data(address)
        except URLError:
            return 404, None
        else:
            code, coords = self.__parse_raw_data(raw_data)
            return code, coords

    def __get_raw_data(self, address):
        """ Helper method to get raw data from service provider

        Args:
            address: address str for which coords are desired

        Returns:
            rawData: a file-like object as reyurned by urlopen()

        """

        query_params = self.api_key_params

        # add address to query_params
        query_params[self.query_address_string] = address

        # construct URL from baseUrl and query_params
        url_string = self.base_url + "?" + urlencode(query_params)

        # get response from service provider API
        return urlopen(url_string)

    def __parse_raw_data(self, raw_data):
        """ Heleper method to parse raw data using api keys params

        Args:
            raw_data: a file-like object from __get_raw_data method

        Returns:
            code, coords: response code and list of corrds

        """

        encoding = raw_data.info().get_content_charset("utf-8")
        raw_code = raw_data.getcode()
        coord_data = raw_data.read()
        coords = json.loads(coord_data.decode(encoding))
        for key in self.coords_keys:
            if not isinstance(key, list):
                try:
                    coords = coords[key]
                except (IndexError, KeyError):
                    return 404, None

        coords = [coords[0], coords[1]]

        return raw_code, coords
