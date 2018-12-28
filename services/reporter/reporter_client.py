from __future__ import print_function

import grpc

import sachima_pb2
import sachima_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('192.168.0.176:50051') as channel:
        stub = sachima_pb2_grpc.ReporterStub(channel)
        response = stub.RunReport(sachima_pb2.ReportRequest(name='r0002'))
    print("Reporter client received: " + response.message)


if __name__ == '__main__':
    run()
