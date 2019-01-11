import inspect
import functools
import importlib
import numpy as np
import pandas as pd
import json
from nameko.rpc import rpc, RpcProxy
from sachima.publish import Publisher


def api(type='grpc', platform='superset'):
    def wrapper(func):
        @functools.wraps(func)
        def api_called(*_args, **kw):
            # before
            _result = func(*_args, **kw)
            # print(_result)  # None
            name = 'r00001'
            # 调用supersetpost注册接口
            Publisher.to(platform, name)
            # after
            return _result
        return api_called
    return wrapper


class Data(object):
    name = 'data'

    @rpc
    def get_report(self, params):
        print(params)
        m = importlib.import_module(params['name'])
        res = m.main()  # dataframe
        return test(res)


def test(data):
    print(type(data[0]))
    return json.dumps({
        'itemDatePicker': [{
            'id': '进件日期',
            'type': 'DatePicker',  # RangePicker
        }, {
            'id': '到期日期',
            'type': 'DateRange',  # RangePicker
        }],
        'itemSelect': [
            {
                'id': '测试1',
                'props': {
                    'mode': 'tags',
                    'allowClear': True,
                    'placeholder': '待输入',
                },
                'option': ['111', 'javascript', 'flutter']
            }, {
                'id': 'Test2',
                'props': {
                    # 'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': [1, 2, 3]
            }, {
                'id': '测试5',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': ['a', 'b', 'c']
            }, {
                'id': '测试4',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': [1]
            }, {
                'id': '测试6',
                'props': {
                    'mode': 'multiple',
                    'allowClear': True,
                    'placeholder': 'pls input',
                },
                'option': []
            },
        ],
        # 'index': data.index.to_frame(),
        'columns': ['a', 'b'],   # data[0].columns.tolist(),
        # data[0].to_json(orient='records', date_format='iso', date_unit='s', force_ascii=False)
        'dataSource': [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        # 'dataSource': data[0].to_dict('records')
    })


def publish(t, p, f, n):
    '''
        class {}(object):
        name = n

        @rpc
        def get(self):
            return f()
    '''

    print('publishing to ' + p + ' using ' + t)
    return 'success'
