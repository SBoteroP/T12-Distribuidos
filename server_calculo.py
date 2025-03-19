import grpc
from concurrent import futures
import archivo_pb2
import archivo_pb2_grpc
import random

class CalculationServicer(archivo_pb2_grpc.CalculationServicer):
    def __init__(self):
        self.op1_channel = grpc.insecure_channel('localhost:50051')
        self.op2_channel = grpc.insecure_channel('localhost:50052')
        self.op1_stub = archivo_pb2_grpc.OperationStub(self.op1_channel)
        self.op2_stub = archivo_pb2_grpc.OperationStub(self.op2_channel)

    def Compute(self, request, context):
        print(f"Received request: {request.a} {request.operation} {request.b}")

        # Alternate between servers
        if random.choice([True, False]):
            response = self.op1_stub.PerformOperation(request)
            print(f"Delegated to Server 1 -> Result: {response.result}")
        else:
            response = self.op2_stub.PerformOperation(request)
            print(f"Delegated to Server 2 -> Result: {response.result}")

        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    archivo_pb2_grpc.add_CalculationServicer_to_server(CalculationServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Calculation Server listening on port 50053...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
