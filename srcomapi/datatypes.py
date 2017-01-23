from .exceptions import APINotProvidedException

class DataType(object):
    @property
    def embeds(self):
        return []

    def __init__(self, srcom=None, data=None, id=None):
        self._api = srcom
        if not self._api:
            raise APINotProvidedException("A SpeedrunCom instance was not passed to the DataType")
        if id and not data:
            self.data = self._api.get("{}/{}".format(self.endpoint, id), params={"embed": ",".join([a.endpoint for a in self.embeds]) if self.embeds else None})
        elif data:
            self.data = data
        else:
            return
        for k,v in self.data.items():
            setattr(self, k, v)
        if self.data:
            for embed in self.embeds:
                if embed.endpoint in self.data and "data" in self.data[embed.endpoint]:
                    self.data[embed.endpoint] = (embed(embed_data) for embed_data in self.data[embed.endpoint]["data"])

    def __repr__(self):
        if "name" in self.data:
            repr_str = """<{clsname} "{name}">"""
        elif "id" in self.data:
            repr_str = """<{clsname} "{id}">"""
        else:
            repr_str = """<{clsname}>"""
        return repr_str.format(clsname=self.__class__.__name__, **self.data)

class Category(DataType):
    endpoint = "categories"

    @property
    def embeds(self):
        return [Game, Variable]

class Developer(DataType):
    endpoint = "developers"

class Engine(DataType):
    endpoint = "engines"

class Game(DataType):
    endpoint = "games"

    @property
    def embeds(self):
        return [Level, Category, Moderator, GameType, Platform, Region, Genre, Engine, Developer, Publisher, Variable]

    def __repr__(self):
        if "names" in self.data and "international" in self.data["names"]:
            return "<Game \"{names[international]}\">".format(**self.data)
        return "<Game \"*unknown*\">"

class GameType(DataType):
    endpoint = "gametypes"

class Genre(DataType):
    endpoint = "genres"

class Guest(DataType):
    endpoint = "guests"

class Leaderboard(DataType):
    endpoint = "leaderboards"

    @property
    def embeds(self):
        return [Game, Category, Level, Player, Region, Platform, Variable]

    def __repr__(self):
        if "data" in self.data["game"]:
            game = self.data["game"]["data"]["names"]["international"]
        else:
            game = self.data["game"]
        if "data" in self.data["category"]:
            category = self.data["category"]["data"]["name"]
        else:
            category = self.data["category"]
        return """<Leaderboard "{}"/"{}">""".format(game, category)

class Level(DataType):
    endpoint = "levels"

    @property
    def embeds(self):
        return [Category, Variable]

class Notification(DataType):
    endpoint = "notifications"

class Platform(DataType):
    endpoint = "platforms"

class Profile(DataType):
    endpoint = "profile"

class Publisher(DataType):
    endpoint = "publishers"

class Region(DataType):
    endpoint = "regions"

class Run(DataType):
    endpoint = "runs"

    @property
    def embeds(self):
        return [Game, Category, Level, Player, Region, Platform]

class Series(DataType):
    endpoint = "series"

    @property
    def embeds(self):
        return [Moderator]

class User(DataType):
    endpoint = "users"

class Moderator(User):
    pass

class Variable(DataType):
    endpoint = "variables"
