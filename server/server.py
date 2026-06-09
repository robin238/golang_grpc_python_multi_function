from concurrent import futures
import grpc
import os
import sys

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# tambahkan root project
sys.path.insert(0, ROOT_DIR)

# tambahkan folder python_pb
sys.path.insert(0, os.path.join(ROOT_DIR, "python_pb"))

from python_pb import service_pb2
from python_pb import service_pb2_grpc

class DemoService(service_pb2_grpc.DemoServiceServicer):

    def Add(self, request, context):
        print("Add Request:", request.a, request.b)

        return service_pb2.AddResponse(
            result=request.a + request.b
        )

    def Uppercase(self, request, context):
        print("Uppercase Request:", request.text)

        return service_pb2.TextResponse(
            result=request.text.upper()
        )

    def Lowercase(self, request, context):
        print("Lowercase Request:", request.text)

        return service_pb2.TextResponse(
            result=request.text.lower()
        )   


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    service_pb2_grpc.add_DemoServiceServicer_to_server(
        DemoService(),
        server
    )

    server.add_insecure_port("0.0.0.0:50051")

    print("Python gRPC Server Running on :50051")

    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()