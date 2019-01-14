from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/osconfeed.json'


def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON, 'wb') as local:
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)


from collections import abc
import keyword

class FrozenJSON:
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value  # for safety
        self.hi = 'jo'

    def __getattr__(self, name):    # is called only when there’s no attribute with that name
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON(self.__data[name])
            # return FrozenJSON.build(self.__data[name])

    # @classmethod
    # def build(cls, obj):
    #     if isinstance(obj, abc.Mapping):
    #         return cls(obj)
    #     elif isinstance(obj, abc.MutableSequence):
    #         return [cls.build(item) for item in obj]
    #     else:
    #         return obj


if __name__ == '__main__':
    # feed = load()
    # l = sorted(feed['Schedule'].keys())
    # print(l)
    # for key, value in sorted(feed['Schedule'].items()):
    #     print('{:3} {}'.format(len(value), key))

    # print(feed['Schedule']['events'][40]['name'])
    # f = FrozenJSON(feed)
    # print(f.Schedule.events[40].name)
    f = FrozenJSON({"a": {"class": 1}})
    print(f.a.class_)
