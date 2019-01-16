from concurrent import futures
import time
import grpc
import sachima_pb2
import sachima_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Reporter(sachima_pb2_grpc.ReporterServicer):
    def setMsg(self, msg):
        self.msg = msg

    def RunReport(self, request, context):
        print(request.params)
        return sachima_pb2.ReportReply(message=str(self.msg))


def serve(msg):
    r = Reporter()
    r.setMsg = msg
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sachima_pb2_grpc.add_ReporterServicer_to_server(r, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
