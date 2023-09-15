**Inactive. Check [the network graph](https://github.com/blha303/srcomapi/network) to see if there are any active forks. Thanks for using srcomapi.**

srcomapi (SpeedrunComAPI) ![travis-ci](https://travis-ci.org/blha303/srcomapi.svg?branch=master)
=========================

A Python 3 implementation of the speedrun.com REST API. `pip3 install srcomapi`

Does not support Python 2. Sorry.

Usage
=====

Start
-----

```python
>>> import srcomapi, srcomapi.datatypes as dt
>>> api = srcomapi.SpeedrunCom(); api.debug = 1
```

Searching for a game
--------------------

```python
# It's recommended to cache the game ID and use it for future requests.
# Data is cached for the current session by classname/id so future
# requests for the same game are instantaneous.
>>> api.search(srcomapi.datatypes.Game, {"name": "super mario sunshine"})
[<Game "Super Mario Sunshine">]
>>> game = _[0]
```

Getting the current world record for a game category
----------------------------------------------------

```python
>>> game.categories
[<Category "Any%">, ...]
>>> _[0].records[0].runs
[{'run': <Run <Game "Super Mario Sunshine">/<Category "Any%">/9mr570dy 4498>, 'place': 1}, ...]
>>> _[0]["run"].times
{'primary_t': 4498, ...}
# primary_t is the time in seconds
```

Getting a dict containing all runs from a game
----------------------------------------------

```python
sms_runs = {}
for category in game.categories:
  if not category.name in sms_runs:
    sms_runs[category.name] = {}
  if category.type == 'per-level':
    for level in game.levels:
      sms_runs[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id)))
  else:
    sms_runs[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(game.id, category.id)))
```
