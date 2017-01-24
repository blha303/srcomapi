import srcomapi
import gzip

def test_api_get_game():
    api = srcomapi.SpeedrunCom()
    assert(api.get_game("sms").name == "Super Mario Sunshine")
