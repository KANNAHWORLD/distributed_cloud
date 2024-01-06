import logging
from concurrent import futures

import grpc

import Terminal_pb2_grpc
import  terminal

import session


# Constants 
PORT = "50051"
MAX_WORKERS = 10

def serve():
    """
    Start the gRPC server and serve requests.

    This function starts a gRPC server with the specified maximum number of workers.
    It adds the `Terminal` class as a servicer to the server and starts the server on the specified port.
    The server is kept alive until termination.

    Args:
        None

    Returns:
        None
    """
    # Instantiate the server with gRPC methods
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
    # To the server which we created, we need to add the class Greeter to the server
    Terminal_pb2_grpc.add_TerminalServicer_to_server(terminal.Terminal(), server)
    
    # This is the port that we are going to use
    server.add_insecure_port("[::]:" + PORT)
    
    # Start the server
    server.start()
    print("Server started, listening on " + PORT)
    logging.log(logging.INFO, "Server started, listening on " + PORT)

    # Keep the server alive until terminations
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()
