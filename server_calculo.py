import grpc
from concurrent import futures
import archivo_pb2
import archivo_pb2_grpc

class CalculationServicer(archivo_pb2_grpc.CalculationServicer):
    def __init__(self):
        # Conectar a los servidores remotos
        self.op1_channel = grpc.insecure_channel('10.43.103.30:50051')
        self.op2_channel = grpc.insecure_channel('10.43.103.102:50052')
        self.op1_stub = archivo_pb2_grpc.OperationStub(self.op1_channel)
        self.op2_stub = archivo_pb2_grpc.OperationStub(self.op2_channel)

    def Compute(self, request, context):
        print(f"Received request: {request.a} {request.operation} {request.b}")

        # Alternar entre servidores según la operación
        if not hasattr(self, "last_server") or self.last_server == "Server 2":
            result = self.perform_operation(self.op1_stub, request.a, request.b, request.operation, "Server 1", '10.43.103.30')
            self.last_server = "Server 1"
        else:
            result = self.perform_operation(self.op2_stub, request.a, request.b, request.operation, "Server 2", '10.43.103.102')
            self.last_server = "Server 2"

        return archivo_pb2.OperationResponse(result=result)

    def perform_operation(self, stub, a, b, operation, server_name, ip):
        """Ejecuta una operación en el servidor especificado o localmente si el servidor falla."""
        try:
            response = stub.PerformOperation(archivo_pb2.OperationRequest(a=a, b=b, operation=operation), timeout=2)
            print(f"✅ {server_name} ({ip}) -> {a} {operation} {b} = {response.result}")
            return response.result
        except grpc.RpcError as e:
            print(f"⚠️ {server_name} ({ip}) no disponible: {e.code()} → Ejecutando localmente")
            return self.perform_local_operation(a, b, operation)

    def perform_local_operation(self, a, b, operation):
        """Ejecuta la operación localmente en caso de fallo de los servidores remotos."""
        if operation == "+":
            return a + b
        elif operation == "-":
            return a - b
        elif operation == "*":
            return a * b
        elif operation == "/":
            return a / b if b != 0 else float('inf')
        else:
            return 0  # Operación no reconocida

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    archivo_pb2_grpc.add_CalculationServicer_to_server(CalculationServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Calculation Server listening on port 50053...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
