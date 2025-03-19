import grpc
from concurrent import futures
import archivo_pb2
import archivo_pb2_grpc

class OperationServicer(archivo_pb2_grpc.OperationServicer):
    def PerformOperation(self, request, context):
        if request.operation == "+":
            result = request.a + request.b
            op_text = "Adding"
        elif request.operation == "-":
            result = request.a - request.b
            op_text = "Subtracting"
        elif request.operation == "*":
            result = request.a * request.b
            op_text = "Multiplying"
        elif request.operation == "/":
            result = request.a / request.b if request.b != 0 else float('inf')
            op_text = "Dividing"
        else:
            return archivo_pb2.OperationResponse(result=0)

        print(f"Processing: {request.a} {request.operation} {request.b} = {result}")
        return archivo_pb2.OperationResponse(result=result)

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    archivo_pb2_grpc.add_OperationServicer_to_server(OperationServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Operation Server listening on port {port}...")
    server.wait_for_termination()

if __name__ == '__main__':
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else "50051"
    serve(port)
