# Geocoding Proxy Service

This is a simple proxy service that can resolve latitude and logitude for a given address using third party geocoding services like [Google](https://developers.google.com/maps/documentation/geocoding/start) and [Here](https://developer.here.com/documentation/geocoder/topics/quick-start.html). Additional services can be added in the services.json file, as per the template of existing services. One of these services can also be declared as primary service provider. For each of the services, the API credentials and secrets need to be provided via the services.secrets.json file. 

The API follows a RESTful HTTP Interface and uses JSON for data serialization.

## Requirements

1. python 3.3+
2. curl (optional for testing only)

## Setup

1. copy services.secrets.json.sample to services.secrets.json
2. Save credentials for geocoding services
    a. **Here**
        - Sign up for an account at https://developer.here.com/authenticationpage
        - Navigate to https://developer.here.com/projects and create a project.
        - On the project page, copy the provided app ID and app Key.
        - Save them into the JSON field `here.api_key_params.app_id` and `here.api_key_params.app_key`, in services.secrets.json.
    b. **Google**
        - Navigate to https://developers.google.com/maps/documentation/geocoding/get-api-key
        - Click "Get a Key" and follow the instructions.
        - Copy the provided API Key.
        - Save it into the JSON field `google.api_key_params.key` in services.secrets.json.
3. OPTIONALLY, add any other third party providers in the services.json file, along with their corresponding credentials/secrets in the services.secrets.json file.

**NOTES** for `services.json` file:

1. Every entry in services.json should have corresponding secrets/credentials entry in the services.secrets.json file.
2. Every entry should provide following _compulsory_ fields:
    a. `base_url`: The URL that is used to make the query service. For example, for google, this would be `https://maps.googleapis.com/maps/api/geocode/json`
    b. `query_address_string`: The query string that is used in the complete http request to service. For eg. for google, the query string is `https://maps.googleapis.com/maps/api/geocode/json/?address=San%20Francisco%2C%20CA&key=YOUR_API_KEY'`, hence this string would be `address`.
    c. `coords_keys`: An ordered sequence of keys and indices from returned json, that could be used to extract `Latitude` and `Longitude` of the address. For example, based on Response example from Here, as outlined [here](https://developer.here.com/documentation/geocoder/topics/quick-start-geocode.html), following sequence of keys can be used for:
    ```
    [
        "Response",
        "View",
        0,
        "Result",
        0,
        "Location",
        "DisplayPosition",
        ["Latitude", "Longitude"]
    ]
    ```

3. Optionally, a `primary` field can be added with a value of "true" (case in-sensitive) to indicate, a particular service needs to be used as a primary service provider. If no service has this field, one of the services is randomly chosen as a primary service provider. If multiple services have this field to be "true", one of those is randomly chosen as the primary service provider.
4. At least 2 service providers are required for this proxy service to work.


## Starting the Proxy Server

The server can be started using the `runProxy.py` python script. By default the service is started at localhost:8088. The server address and the port can be modified using the optional arguments `--server` and `--port`.

```bash
./runProxy.py --help

usage: runProxy.py [-h] [-s SERVER] [-p PORT]

Run GeoCode Proxy Server

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Server Address (default='0.0.0.0')
  -p PORT, --port PORT  Server Port (default=8088)
```

For example, we can start the server on http://localhost:9099/ as,

```bash
./runProxy.py --server localhost --port 9099

Server is running at http://localhost:9099
```

The service can be graciously killed by sending SIGINT via the CNTRL+C (^C) key stroke. 

## Testing the API

Since the API provides a RESTful HTTP Interface, it can be used by different web clients.

Assuming, we started our server as above on http://localhost:9099, queries can be made as follows: `http://localhost:9099/?address=San%20Francisco%2C%20CA`.

1. Use curl to make a request:

```bash
curl "http://localhost:9099/?address=San%20Francisco%2C%20CA"

{"Latitude": 37.77713, "Longitude": -122.41964}
```

2. You can paste `http://localhost:9099/?address=San%20Francisco%2C%20CA` in  your browser.

3. You can use the provided helper script `testProxy.py`. This script first tries to use `curl` to make a query. If curl is not found, it uses the [`urllib.request.urlopen()`](https://docs.python.org/3/library/urllib.request.html) method from the standard python library to make a query. It takes "address" as a positional argument and optionally lets you chose the server address and port, using the `--server` and `--port` options, same as the `runProxy.py` script.

```bash
./testProxy.py --help

usage: testProxy.py [-h] [-s SERVER] [-p PORT] address

Test GeoCode Proxy Server

positional arguments:
  address               Address for which Geo Corrds are needed

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Server Address (default='localhost')
  -p PORT, --port PORT  Server Port (default=8088)
```

Example run:

```bash
./testProxy.py "San Francisco, CA" --server localhost --port 9099

Running...
'curl http://localhost:8088/?address=San%20Francisco%2C%20CA'
{"Latitude": 37.77713, "Longitude": -122.41964}%
```


## Tests

The tests can be run as follows:

```bash
python3 -m unittest

....Using Service: here...
Using Service: google...
.Using Service: here...
Using Service: google...
.Using Service: here...
.Using Service: google...
Using Service: here...
.Using Service: google...
.Using Service: google...
.Using Service: here...
Using Service: google...
.Using Service: here...
.
----------------------------------------------------------------------
Ran 12 tests in 2.296s

OK
```

## Future Work

1. Proxy server could use caching for last N address calls, reducing number of external API calls. (A simple implementation can be found in the `cached` branch.)
2. Better logging with some third party python libraries
