import requests
from http.client import responses
from os.path import dirname
from os import environ
import inspect

import srcomapi
import srcomapi.datatypes as datatypes
from .exceptions import APIRequestException, APINotProvidedException

# libraries for mocking
import json
import gzip

with open(dirname(srcomapi.__file__) + "/.version") as f:
    __version__ = f.read().strip()
API_URL = "https://www.speedrun.com/api/v1/"
TEST_DATA = dirname(srcomapi.__file__) + "/test_data/"

class SpeedrunCom(object):
    def __init__(self, api_key=None, user_agent="blha303:srcomapi/"+__version__, mock=False):
        self._datatypes = {v.endpoint:v for k,v in inspect.getmembers(datatypes, inspect.isclass) if hasattr(v, "endpoint")}
        self.api_key = api_key
        self.user_agent = user_agent
        self.mock = mock
        self.debug = 0

    def get(self, endpoint, **kwargs):
        headers = {"User-Agent": self.user_agent}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        kwargs.update({"headers": headers})
        uri = API_URL + endpoint
        if self.debug >= 1: print(uri)
        if self.mock:
            mock_endpoint = ".".join(endpoint.split("/")[0::2])
            try:
                with gzip.open(TEST_DATA + mock_endpoint + ".json.gz") as f:
                    data = json.loads(f.read().decode("utf-8"))["data"]
            except FileNotFoundError:
                response = requests.get(uri, **kwargs)
                if response.status_code != 404:
                    with gzip.open(TEST_DATA + mock_endpoint + ".json.gz", "wb") as f:
                        """SRC allows to 200 entries max per request 
                        so we're making requests until we get all entries
                        https://github.com/speedruncomorg/api/blob/master/version1/pagination.md
                        """
                        json_to_write = response.json()
                        data = response.json()["data"]
                        try:
                            response_size = response.json()['pagination']['size']
                            response_max_size = response.json()['pagination']['max']
                            while response_size == response_max_size: #if request size is the maximum allowed we haven't reached the end of entries
                                uri = response.json()['pagination']['links'][0]["uri"] #SRC gives us the link to use for next request
                                response = requests.get(uri)
                                response_size = response.json()['pagination']['size']
                                response_max_size = response.json()['pagination']['max']
                                data.extend(response.json()["data"])
                        except KeyError:
                            pass
                        json_to_write['data'] = data
                        f.write(json.dumps(json_to_write).encode("utf-8"))
                else:
                    raise APIRequestException((response.status_code, responses[response.status_code], uri[len(API_URL):]), response)
        else:
            response = requests.get(uri, **kwargs)
            if response.status_code > 400:
                raise APIRequestException((response.status_code, responses[response.status_code], uri[len(API_URL):]), response)
            data = response.json()["data"]
            try:
                response_size = response.json()['pagination']['size']
                response_max_size = response.json()['pagination']['max']
                while response_size == response_max_size: 
                    uri = response.json()['pagination']['links'][0]["uri"] 
                    response = requests.get(uri)
                    response_size = response.json()['pagination']['size']
                    response_max_size = response.json()['pagination']['max']
                    data.extend(response.json()["data"])
            except KeyError:
                pass
        return data

    def get_game(self, id, **kwargs):
        return datatypes.Game(self, data=self.get("games/" + id))

    def get_games(self, **kwargs):
        """ Legacy function, will be removed in next major version"""
        return self.search(datatypes.Game, **kwargs)

    def get_user(self, id, **kwargs):
        return datatypes.User(self, data=self.get("users/" + id))

    def search(self, datatype, params):
        """Returns a generator that uses the given datatype and search params to get results"""
        response = self.get(datatype.endpoint, params=params)
        return [datatype(self, data=data) for data in response]
