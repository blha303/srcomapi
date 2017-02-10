from .exceptions import APINotProvidedException

class DataType(object):
    def __init__(self, srcom=None, data=None, id=None, position=None):
        if self.__class__.__name__ == "Moderator":
            self.position = position
        self._retrieved = []
        self._api = srcom
        if not self._api:
            raise APINotProvidedException("A SpeedrunCom instance was not passed to the DataType")
        if id and not data:
            self.data = self._api.get("{}/{}".format(self.endpoint, id))
        elif data:
            self.data = data
        if self.data:
            for embed in self.embeds:
                if hasattr(embed, "_embed_name"):
                    endpoint = embed._embed_name
                elif hasattr(embed, "endpoint"):
                    endpoint = embed.endpoint
                else:
                    continue
                if endpoint in self.data and "data" in self.data[endpoint]:
                    self.data[endpoint] = (embed(embed_data) for embed_data in self.data[endpoint]["data"])

    def __getattr__(self, attr):
        if "_" in attr:
            attr = attr.replace("_", "-")
        if not hasattr(self, "data"):
            raise AttributeError("No data in datatype")
        if self._api.debug: print("__getattr__: " + attr)
        if attr in self.data:
            if attr in self._api._datatypes:
                cls = self._api._datatypes[attr]
                if type(self.data[attr]) is list and len(self.data[attr]) > 0 and len(self.data[attr][0]) == 8:
                    self.data[attr] = [cls(self._api, id=id) for id in self.data[attr]]
                    self._retrieved.append(attr)
                elif type(self.data[attr]) is str and len(self.data[attr]) == 8:
                    self.data[attr] = cls(self._api, id=self.data[attr])
                    self._retrieved.append(attr)
            return self.data[attr]
        raise AttributeError("{} is not in {}".format(attr, self.data))

    def __repr__(self):
        if "name" in self.data:
            repr_str = """<{clsname} "{name}">"""
        elif "id" in self.data:
            repr_str = """<{clsname} "{id}">"""
        else:
            return """<{clsname}>""".format(clsname=self.__class__.__name__)
        return repr_str.format(clsname=self.__class__.__name__, **self.data)

    def __dir__(self):
        import inspect
        out = [i[0] for i in inspect.getmembers(self.__class__)] + (list(self.data.keys()) if self.data else []) + list(self.__dict__.keys())
        return [a.replace("-", "_") for a in out]

    @property
    def embeds(self):
        return []

class Category(DataType):
    endpoint = "categories"

    @property
    def variables(self):
        name = "variables"
        if name in self._retrieved:
            return self.data[name]
        data = [Variable(self._api, data=d) for d in self._api.get("{}/{}/{}".format(self.endpoint, self.id, name))]
        self.data[name] = data
        self._retrieved.append(name)
        return data

    @property
    def records(self):
        name = "records"
        if name in self._retrieved and name in self.data:
            return self.data[name]
        data = [Leaderboard(self._api, data=d) for d in self._api.get("{}/{}/{}".format(self.endpoint, self.id, name))]
        self.data[name] = data
        self._retrieved.append(name)
        return data

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
    def name(self):
        return self.data["names"]["international"]

    @property
    def categories(self):
        name = "categories"
        if name in self._retrieved:
            return self.data[name]
        data = [Category(self._api, data=d) for d in self._api.get("{}/{}/{}".format(self.endpoint, self.id, name))]
        self.data[name] = data
        self._retrieved.append(name)
        return data

    @property
    def levels(self):
        name = "levels"
        if name in self._retrieved:
            return self.data[name]
        data = [Level(self._api, data=d) for d in self._api.get("{}/{}/{}".format(self.endpoint, self.id, name))]
        self.data[name] = data
        self._retrieved.append(name)
        return data

    @property
    def moderators(self):
        name = "moderators"
        if name in self._retrieved:
            return self.data[name]
        data = [Moderator(self._api, id=id, position=position) for id,position in self.data[name].items()]
        self.data[name] = data
        self._retrieved.append(name)
        return data

    @property
    def variables(self):
        name = "variables"
        if name in self._retrieved:
            return self.data[name]
        data = [Variable(self._api, data=d) for d in self._api.get("{}/{}/{}".format(self.endpoint, self.id, name))]
        self.data[name] = data
        self._retrieved.append(name)
        return data

    @property
    def derived_games(self):
        name = "derived-games"
        if name in self._retrieved:
            return self.data[name]
        data = [Game(self._api, data=d) for d in self._api.get("{}/{}/{}".format(self.endpoint, self.id, "derived-games"))]
        self.data[name] = data
        self._retrieved.append(name)
        return data

    @property
    def records(self):
        name = "records"
        if name in self._retrieved:
            return self.data[name]
        data = [Leaderboard(self._api, data=d) for d in self._api.get("{}/{}/{}".format(self.endpoint, self.id, name))]
        self.data[name] = data
        self._retrieved.append(name)
        return data

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

class Leaderboard(DataType):
    endpoint = "leaderboards"

    @property
    def embeds(self):
        return [Game, Category, Level, Player, Region, Platform, Variable]

    @property
    def runs(self):
        name='runs'
        if name in self._retrieved:
            return self.data[name]
        for run in self.data[name]:
            run['run']=Run(self._api,data=run['run'])
        self._retrieved.append(name)
        return self.data[name]

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

class Player(DataType):
    endpoint = "users"

class Guest(Player):
    endpoint = "guests"

class User(Player):
    pass

class Moderator(User):
    _embed_name = "moderators"

class Profile(DataType):
    endpoint = "profile"

class Publisher(DataType):
    endpoint = "publishers"

class Region(DataType):
    endpoint = "regions"

class Run(DataType):
    endpoint = "runs"

    @property
    def players(self):
        if "players" in self._retrieved:
            return self.data["players"]
        p = []
        for player in self.data["players"]:
            if player["rel"] == "user":
                p.append(User(self._api, id=player['id']))
            elif player["rel"] == "guest":
                p.append(Guest(self._api, id=player['name']))
            else:
                #should never be reached
                p.append(Player(self._api, id=player['id']))
        self.data["players"] = p
        self._retrieved.append('players')
        return p

    @property
    def embeds(self):
        return [Game, Category, Level, Player, Region, Platform]

class Series(DataType):
    endpoint = "series"

    @property
    def embeds(self):
        return [Moderator]

class Variable(DataType):
    endpoint = "variables"
