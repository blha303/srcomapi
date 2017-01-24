import srcomapi

def setup_api():
    return srcomapi.SpeedrunCom(mock=True)

def test_speedruncom_get_game():
    api = setup_api()
    assert(api.get_game("sms").name == "Super Mario Sunshine")

def test_game():
    api = setup_api()
    game = srcomapi.datatypes.Game(api, id=id)
    assert(game.name == "Super Mario Sunshine")
    assert(game.abbreviation == "sms")
