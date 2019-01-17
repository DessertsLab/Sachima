import inspect
import functools
import importlib
import os
import numpy as np
import pandas as pd
import json
from nameko.rpc import rpc, RpcProxy
from sachima.publish import Publisher
from sachima.params import Filter, data_wrapper


def api(platform="superset", isRun=False, **kw_api):
    def wrapper(func):
        @functools.wraps(func)
        def api_called(*args, **kw):

            # 调用对应注册接口
            if platform == "superset":
                fpath = inspect.getfile(func)
                fname = os.path.split(fpath)[1]
                fmod = os.path.splitext(fname)[0]
                Publisher.to_superset(
                    name=kw_api.get("name", fmod),
                    type_=kw_api.get("type_", "RPC"),
                    param=fmod,
                )
            else:
                pass

            # 默认不运行
            if isRun:
                _result = func(*args, **kw)
                return _result

        return api_called

    return wrapper


class Data(object):
    name = "data"

    @rpc
    def get_report(self, params):
        m = importlib.import_module(params["name"])
        return data_wrapper(m.main(params))
