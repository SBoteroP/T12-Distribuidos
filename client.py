import grpc
import archivo_pb2
import archivo_pb2_grpc

def run():
    # Conectar al servidor de cálculo en una IP remota
    server_ip = "10.43.103.204"  
    channel = grpc.insecure_channel(f"{server_ip}:50053")
    stub = archivo_pb2_grpc.CalculationStub(channel)

    while True:
        try:
            # Obtener entrada del usuario
            expr = input("Enter an expression with three operations (e.g., '10 + 5 * 2') or 'q' to quit: ").strip()
            if expr.lower() == 'q':
                break

            # Analizar la entrada (por ejemplo, "10 + 5 * 2")
            tokens = expr.split()
            if len(tokens) != 5:
                print("Invalid format! Use: number operator number operator number")
                continue
            
            # Extraer valores
            a = float(tokens[0])
            op1 = tokens[1]
            b = float(tokens[2])
            op2 = tokens[3]
            c = float(tokens[4])

            if op1 not in "+-*/" or op2 not in "+-*/":
                print("Invalid operator! Use + - * /")
                continue
            
            # Primera operación
            request1 = archivo_pb2.OperationRequest(a=a, b=b, operation=op1)
            response1 = stub.Compute(request1)
            intermediate_result = response1.result

            # Segunda operación
            request2 = archivo_pb2.OperationRequest(a=intermediate_result, b=c, operation=op2)
            response2 = stub.Compute(request2)

            # Mostrar resultado final
            print(f"Final Result: ({a} {op1} {b}) {op2} {c} = {response2.result}\n")

        except ValueError:
            print("Invalid input! Try again.")
        except grpc.RpcError as e:
            print(f"⚠️ Error connecting to server ({server_ip}): {e.code()}")
            break

if __name__ == '__main__':
    run()
