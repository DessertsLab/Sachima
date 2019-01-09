import inspect
import functools
import sanic
from sachima.services import server
import numpy as np
import pandas as pd
import json

################################


def get_data(r):
    if r == 'r0001':
        data = pd.DataFrame({
            '0': 1.,
            'test1': '20181228',
            'test2': '这是一段测试文字测试字段的长度是否能自动调整',
        })
    else:
        data = pd.DataFrame({
            '0': 1.,
            '字段A': '20181228',
            '字段B': '这是一段测试文字测试字段的长度是否能自动调整',
            '字段C': pd.Series(1, index=list(range(4)), dtype='float32'),
            '字段D': np.array([3] * 4, dtype='int32'),
            '字段E': pd.Categorical(["test", "train", "test", "train"]),
            '字段F': '这是一段测试文字测试字段的长度是否能自动调整',
            '字段G': '这是一段测试文字测试字段的长度是否能自动调整这是一段测试' +
            '文字测试字段的长度是否能自动调整这是一段测试文字测试字段的长度是否能自动调整'
        })

    return json.dumps({
        'itemDatePicker': {
            'id': '日期',
            'type': 'DatePicker',  # RangePicker
        },
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
        'columns': data.columns.tolist(),
        'dataSource': data.to_dict('records')
    })




server.serve(get_data(''))

def api(type='grpc', platform='superset'):
    def wrapper(func):
        @functools.wraps(func)
        def api_called(*_args, **kw):
            # before
            _result = func(*_args, **kw)
            # print(_result)  # None
            publish(type, platform)
            # 调用supersetpost注册接口

            # after
            return _result
        return api_called
    return wrapper


def publish(t, p):
    print('publishing to ' + p + ' using ' + t)
    return 'success'
