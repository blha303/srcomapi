import srcomapi

def test_api_get_game():
    api = srcomapi.SpeedrunCom()
    assert(next(api.get_game("sms")).name == "Super Mario Sunshine")
