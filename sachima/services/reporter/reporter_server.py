from concurrent import futures
import time

import grpc

import sachima_pb2
import sachima_pb2_grpc

import numpy as np
import pandas as pd

import json

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


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


class Reporter(sachima_pb2_grpc.ReporterServicer):
    def RunReport(self, request, context):
        msg = get_data(request.params)
        print(request.params)
        return sachima_pb2.ReportReply(message=str(msg))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sachima_pb2_grpc.add_ReporterServicer_to_server(Reporter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
