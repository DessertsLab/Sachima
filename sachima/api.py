import inspect
import functools
import importlib
import numpy as np
import pandas as pd
import json
from nameko.rpc import rpc, RpcProxy
from sachima.publish import Publisher
from sachima.params import Filter, DataWrapper


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
        print(params)
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
        return DataWrapper(res)


def test(data):
    print(type(data[0]))
    return json.dumps(
        {
            "itemDatePicker": [
                {"id": "日期", "type": "DatePicker", "props": {"size": "small"}},
                {"id": "日期", "type": "RangePicker", "props": {"size": "small"}},
            ],
            "itemSelect": [
                {
                    "id": "noshoptype",
                    "props": {"mode": "tags", "allowClear": True, "placeholder": "待输入"},
                    "option": ["TEST", ""],
                },
                {
                    "id": "Test2",
                    "props": {
                        # 'mode': 'multiple',
                        "allowClear": True,
                        "placeholder": "pls input",
                    },
                    "option": [1, 2, 3],
                },
                {
                    "id": "行业类型",
                    "props": {
                        "mode": "multiple",
                        "allowClear": True,
                        "placeholder": "pls input",
                    },
                    "option": ["医美", "祛痘", "其它"],
                },
                {
                    "id": "测试4",
                    "props": {
                        "mode": "multiple",
                        "allowClear": True,
                        "placeholder": "pls input",
                    },
                    "option": [1],
                },
                {
                    "id": "测试6",
                    "props": {
                        "mode": "multiple",
                        "allowClear": True,
                        "placeholder": "pls input",
                    },
                    "option": [],
                },
            ],
            # 'index': data.index.to_frame(),
            "columns": ["a", "b"],  # data[0].columns.tolist(),
            # data[0].to_json(orient='records', date_format='iso', date_unit='s', force_ascii=False)
            "dataSource": [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
            # 'dataSource': data[0].to_dict('records')
        }
    )
