import grpc
import archivo_pb2
import archivo_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50053')
    stub = archivo_pb2_grpc.CalculationStub(channel)

    while True:
        try:
            # Get user input
            expr = input("Enter an expression with three operations (e.g., '10 + 5 * 2') or 'q' to quit: ").strip()
            if expr.lower() == 'q':
                break

            # Parse the input (e.g., "10 + 5 * 2")
            tokens = expr.split()
            if len(tokens) != 5:
                print("Invalid format! Use: number operator number operator number")
                continue
            
            # Extract values
            a = float(tokens[0])
            op1 = tokens[1]
            b = float(tokens[2])
            op2 = tokens[3]
            c = float(tokens[4])

            if op1 not in "+-*/" or op2 not in "+-*/":
                print("Invalid operator! Use + - * /")
                continue
            
            # First operation
            request1 = archivo_pb2.OperationRequest(a=a, b=b, operation=op1)
            response1 = stub.Compute(request1)
            intermediate_result = response1.result

            # Second operation
            request2 = archivo_pb2.OperationRequest(a=intermediate_result, b=c, operation=op2)
            response2 = stub.Compute(request2)

            # Show final result
            print(f"Final Result: ({a} {op1} {b}) {op2} {c} = {response2.result}\n")

        except ValueError:
            print("Invalid input! Try again.")

if __name__ == '__main__':
    run()
