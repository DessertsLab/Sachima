from __future__ import print_function

import grpc

import sachima_pb2
import sachima_pb2_grpc


API_PARAMES = {"reportname": "r0001", "字段C": [1, 2, 3]}


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("0.0.0.0:50051") as channel:
        stub = sachima_pb2_grpc.ReporterStub(channel)
        response = stub.RunReport(
            sachima_pb2.ReportRequest(params=str(API_PARAMES))
        )
    print("Reporter client received: " + response.message)


if __name__ == "__main__":
    run()
