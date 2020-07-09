from sachima import config

conf = {}
for key in dir(config):
    if key.isupper():
        conf[key] = getattr(config, key)

from .cli import sachima