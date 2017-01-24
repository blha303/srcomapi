import srcomapi
import gzip
import json

def load(fn):
    with gzip.open("test_data/{}.json.gz".format(fn)) as f:
        return json.loads(f.read().decode("utf-8"))["data"]

def setup_game():
    data = load("games")
    api = srcomapi.SpeedrunCom()
    return srcomapi.datatypes.Game(api, data=data)

def test_api_get_game():
    api = srcomapi.SpeedrunCom()
    assert(api.get_game("sms").name == "Super Mario Sunshine")

def test_game():
    game = setup_game()
    assert(game.name == "Super Mario Sunshine")
    assert(game.abbreviation == "sms")
