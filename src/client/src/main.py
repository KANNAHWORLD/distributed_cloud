
import logging

import grpc
import Terminal_pb2_grpc as Terminal_pb2_grpc
import Terminal_pb2 as Terminal_pb2

def run():
    """
    Function to establish a connection with the gRPC server and send a ping request.
    """
    
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = Terminal_pb2_grpc.TerminalStub(channel)

        response = stub.ping(Terminal_pb2.MyRequest())
        
        print("Recieved response: " + response.message + " {response.alive}")
        
    # print("Greeter client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run()
