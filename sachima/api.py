import inspect
import functools
import sanic


def api(type='grpc', platform='superset'):
    def wrapper(func):
        def api_called(*_args, **kw):
            # before
            _result = func(*_args, **kw)
            # print(_result)  # None
            publish(type, platform)
            # after
            return _result
        return api_called
    return wrapper


def publish(t, p):
    print('publishing to ' + p + ' using ' + t)
    return 'success'
