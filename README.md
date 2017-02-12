srcomapi (SpeedrunComAPI) ![travis-ci](https://travis-ci.org/blha303/srcomapi.svg?branch=master)
=========================

A Python implementation of the speedrun.com REST API

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
# It's recommended to cache the game ID and use it for future requests
>>> api.search(srcomapi.datatypes.Game, {"name": "super mario sunshine"})
[<Game "Super Mario Sunshine">]
>>> game = _[0]
```

Getting the current world record for a game category
----------------------------------------------------

```python
>>> game.categories
[<Category "Any%">, <Category "All Level Shines">, <Category "All Shines, No Blues">, <Category "120 Shines">, <Category "Any% No Major Skips">, <Category "All Episodes">, <Category "20 Shines">, <Category "Individual Shines">, <Category "Individual Worlds">]
# Getting the world record for the Any% category
>>> _[0].records[0].runs
[{'run': <Run "9mr570dy">, 'place': 1}, {'run': <Run "7z02ng9m">, 'place': 2}, {'run': <Run "8y8619xm">, 'place': 3}]
>>> _[0]["run"].times
{'ingame_t': 0, 'realtime_noloads': None, 'primary_t': 4498, 'realtime_noloads_t': 0, 'realtime': 'PT1H14M58S', 'primary': 'PT1H14M58S', 'ingame': None, 'realtime_t': 4498}
# primary_t is the time in seconds
```
