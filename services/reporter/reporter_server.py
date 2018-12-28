from concurrent import futures
import time

import grpc

import sachima_pb2
import sachima_pb2_grpc

import numpy as np
import pandas as pd

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def get_data(r):
    if r == 'r0001':
        data = pd.DataFrame({
            '0': 1.,
            'test1': pd.Timestamp('20181228'),
            'test2': '这是一段测试文字测试字段的长度是否能自动调整',
        })
    else:
        data = pd.DataFrame({
            '0': 1.,
            '字段A': pd.Timestamp('20181228'),
            '字段B': '这是一段测试文字测试字段的长度是否能自动调整',
            '字段C': pd.Series(1, index=list(range(4)), dtype='float32'),
            '字段D': np.array([3] * 4, dtype='int32'),
            '字段E': pd.Categorical(["test", "train", "test", "train"]),
            '字段F': '这是一段测试文字测试字段的长度是否能自动调整'
        })

    col_width = 1 / len(data.columns)

    return {'you send: ': r,
            'itemSelect': {
                '字段A': ['111', 'javascript', 'flutter'],
                '字段C': [1, 2, 3],
                '测试3': ['a', 'b', 'c'],
                '字段D': [1],
                '字段E': [''],
            },
            'columns': list(map(
                lambda x: {
                    'title': x,
                    'dataIndex': x,
                    'key': x,
                    'width': f'{col_width:.0%}'
                },
                data.columns.tolist()
            )),
            'dataSource': list(data.reset_index().rename(
                columns={'index': 'key'}).T.to_dict().values())
            }


class Reporter(sachima_pb2_grpc.ReporterServicer):
    def RunReport(self, request, context):
        msg = get_data(request.params)
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
    # get_data()
