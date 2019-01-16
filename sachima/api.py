import inspect
import functools
import importlib
import numpy as np
import pandas as pd
import json
from nameko.rpc import rpc, RpcProxy
from sachima.publish import Publisher
from sachima.params import Filter, data_wrapper


def api(type="grpc", platform="superset"):
    def wrapper(func):
        @functools.wraps(func)
        def api_called(*_args, **kw):
            # before
            _result = func(*_args, **kw)
            name = inspect.getfile(func)
            # 调用supersetpost注册接口
            Publisher.to(platform, name)
            # after
            return _result

        return api_called

    return wrapper


class Data(object):
    name = "data"

    @rpc
    def get_report(self, params):
        m = importlib.import_module(params["name"])
        return data_wrapper(m.main(params))
