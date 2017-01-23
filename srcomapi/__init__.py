import inspect

from srcomapi import srcomapi, datatypes, exceptions
SpeedrunCom = srcomapi.SpeedrunCom

def cls(module):
    return [i[0] for i in inspect.getmembers(module, inspect.isclass)]

__all__ = cls(srcomapi) + cls(datatypes) + cls(exceptions)
