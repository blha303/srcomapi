import requests
from http.client import responses
from os.path import dirname

import srcomapi
from .datatypes import *
from .exceptions import APIRequestException, APINotProvidedException

with open(dirname(srcomapi.__file__) + "/.version") as f:
    __version__ = f.read().strip()
API_URL = "https://www.speedrun.com/api/v1/"

class SpeedrunCom(object):
    def __init__(self, api_key=None, user_agent="blha303:srcomapi/"+__version__):
        self.api_key = api_key
        self.user_agent = user_agent

    def get(self, endpoint, **kwargs):
        headers = {"User-Agent": self.user_agent}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        response = requests.get(API_URL + endpoint, params=kwargs, headers=headers)
        if response.status_code == 404:
            raise APIRequestException("{} {}".format(response.status_code, responses[response.status_code]), response)
        return response.json()["data"]

    def get_game(self, id=None, **kwargs):
        """Returns a generator that yields srcomapi.Game objects containing the response data"""
        if not "embed" in kwargs:
            kwargs["embed"] = "categories"
        response = self.get("games" + ("/{}".format(id) if id else ""), **kwargs)
        if type(response) is list:
            for game_data in response:
                yield Game(self, game_data)
        elif type(response) is dict:
            yield Game(self, response)

    def get_games(self, **kwargs):
        """Returns a generator (via SpeedrunCom.get_game) that yields srcomapi.Game objects containing the response data."""
        return get_game(id=None, **kwargs)
