"""
Unit Tests for geoLocateProxy API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This file provides a set of tests for various components of this API

"""

from unittest import TestCase

from geoCoder import GeoCoder
from geoCoder.externalServiceProvider import ExternalServiceProvider

ADDRESS = "San Francisco, CA"
GOOGLE_COORDS = [37.7749295, -122.4194155]
HERE_COORDS = [37.77713, -122.41964]


class TestGeoCoder(TestCase):
    """ Test class for GeoCoder class """

    def test_google_service(self):
        """ Test if Google Service is working correctly"""

        geocoder = GeoCoder()

        # make google as primary
        gs = [x for x in geocoder.services if x.name == 'google'][0]
        hs = [x for x in geocoder.services if x.name == 'here'][0]
        geocoder.services = [gs, hs]

        status, coords = geocoder.get_geocode(ADDRESS)

        assert geocoder.services[0].name == 'google'
        assert status == 200
        assert coords == GOOGLE_COORDS

    def test_here_service(self):
        """ Test if Here Service is working correctly"""

        geocoder = GeoCoder()

        # make here as primary
        gs = [x for x in geocoder.services if x.name == 'google'][0]
        hs = [x for x in geocoder.services if x.name == 'here'][0]
        geocoder.services = [hs, gs]

        status, coords = geocoder.get_geocode(ADDRESS)

        assert geocoder.services[0].name == 'here'
        assert status == 200
        assert coords == HERE_COORDS

    def test_here_primary_down(self):
        """ Test if Here is Primary and down"""

        geocoder = GeoCoder()

        # make here as primary
        gs = [x for x in geocoder.services if x.name == 'google'][0]
        hs = [x for x in geocoder.services if x.name == 'here'][0]
        geocoder.services = [hs, gs]

        # make here down by changing its url
        geocoder.services[0].base_url = ""

        status, coords = geocoder.get_geocode(ADDRESS)

        assert geocoder.services[0].name == 'here'
        assert status == 200
        assert coords == GOOGLE_COORDS

    def test_google_primary_down(self):
        """ Test if Google is Primary and down"""

        geocoder = GeoCoder()

        # make here as primary
        gs = [x for x in geocoder.services if x.name == 'google'][0]
        hs = [x for x in geocoder.services if x.name == 'here'][0]
        geocoder.services = [gs, hs]

        # make here down by changing its url
        geocoder.services[0].base_url = ""

        status, coords = geocoder.get_geocode(ADDRESS)

        assert geocoder.services[0].name == 'google'
        assert status == 200
        assert coords == HERE_COORDS

    def test_here_not_primary_down(self):
        """ Test if Here is NOT Primary and down"""

        geocoder = GeoCoder()

        # make here as primary
        gs = [x for x in geocoder.services if x.name == 'google'][0]
        hs = [x for x in geocoder.services if x.name == 'here'][0]
        geocoder.services = [gs, hs]

        # make here down by changing its url
        geocoder.services[1].base_url = ""

        status, coords = geocoder.get_geocode(ADDRESS)

        assert geocoder.services[0].name == 'google'
        assert status == 200
        assert coords == GOOGLE_COORDS

    def test_google_not_primary_down(self):
        """ Test if Google is NOT Primary and down"""

        geocoder = GeoCoder()

        # make here as primary
        gs = [x for x in geocoder.services if x.name == 'google'][0]
        hs = [x for x in geocoder.services if x.name == 'here'][0]
        geocoder.services = [hs, gs]

        # make here down by changing its url
        geocoder.services[1].base_url = ""

        status, coords = geocoder.get_geocode(ADDRESS)

        assert geocoder.services[0].name == 'here'
        assert status == 200
        assert coords == HERE_COORDS

    def test_both_services_down(self):
        """ Test if both services are down"""

        geocoder = GeoCoder()

        # make here down by changing its url
        geocoder.services[1].base_url = "https://maps.googleapis.com"
        geocoder.services[0].base_url = "https://geocoder.cit.com"

        status, coords = geocoder.get_geocode(ADDRESS)

        assert status == 503
        self.assertIsNone(coords)

    def test_bad_address(self):
        """ Test if bad address is used """

        geocoder = GeoCoder()

        status, coords = geocoder.get_geocode("/")

        assert status == 404
        self.assertIsNone(coords)

class TestExternalServiceProvider(TestCase):
    """ Test class for ExternalServiceProvider class """

    def test_missing_coords_keys(self):
        """ Test if coords keys are missing for parsing coords """

        geocoder = GeoCoder()

        service = geocoder.services[0]

        # modify key for KeyError
        coords_keys = service.coords_keys
        coords_keys[1] = "View2"

        status, coords = service.get_geocode(ADDRESS)

        assert status == 404
        self.assertIsNone(coords)

        # modify key for ValueError
        coords_keys[1] = "View"
        coords_keys[2] = 8

        status, coords = service.get_geocode(ADDRESS)

        assert status == 404
        self.assertIsNone(coords)

    def test_wrong_order_coords_keys(self):
        """ Test if coords keys are incorrectly ordered for parsing coords """

        geocoder = GeoCoder()

        service = geocoder.services[0]

        # modify key order
        coords_keys = service.coords_keys
        temp = coords_keys[1]
        coords_keys[1] = coords_keys[2]
        coords_keys[2] = temp

        status, coords = service.get_geocode(ADDRESS)

        assert status == 404
        self.assertIsNone(coords)

    def test_incorrect_lat_here_keys(self):
        """ Test if coords keys for lat, long are incorrect for Here """

        geocoder = GeoCoder()

        # test for Here service
        service = geocoder.services[0]

        # modify key order
        coords_keys = service.coords_keys
        lkeys = coords_keys[-1]
        lkeys[0] = "Latitudes"
        lkeys[1] = "Longitudes"
        coords_keys[-1] = lkeys

        self.assertRaises(KeyError, service.get_geocode, ADDRESS)

    def test_incorrect_lat_google_keys(self):
        """ Test if coords keys for lat, long are incorrect for Google """

        geocoder = GeoCoder()

        # test for Google service
        service = geocoder.services[1]

        # modify key order
        coords_keys = service.coords_keys
        lkeys = coords_keys[-1]
        lkeys[0] = "Lats"
        lkeys[1] = "Longs"
        coords_keys[-1] = lkeys

        self.assertRaises(KeyError, service.get_geocode, ADDRESS)
