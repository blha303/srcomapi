srcomapi (SpeedrunComAPI) ![travis-ci](https://travis-ci.org/blha303/srcomapi.svg?branch=master)
=========================

A Python implementation of the speedrun.com REST API.

Usage
=====

Start
-----

```python
>>> import srcomapi
>>> api = srcomapi.SpeedrunCom()
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
