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
            # print(_result)  # None
            name = "r00001"
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
        print(params)  # {'name': 'email_content_style_example', 'params': {}}
        m = importlib.import_module(params["name"])
        # print(params['params']['日期'])

        """
        {
        'ApiUrl': 'http://0.0.0.0:8080/api/v1/reports/test1',
        '日期': '2019-01-01T05:33:03.801Z',
        '日期1': '2019-01-16T05:33:06.118Z',
        '测试1': ['111', 'flutter'],
        'Test2': 2,
        '测试5': ['b', 'c']
        }
        """
        res = m.main(params["params"])  # dataframe
        return data_wrapper(res)
