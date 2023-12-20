
from concurrent import futures
import logging

import grpc
import basics_pb2
import basics_pb2_grpc


# This is your own defined function
# the parameter input is the thing that we want to start off by passing in 
class Greeter(basics_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(request.hello)
        reply = basics_pb2.HelloReply()
        reply.serverMessage = "Hello, Sid"
        reply.randomNumber = 100
        
        return reply
        
class StockBuyer(basics_pb2_grpc.StockBuyerServicer):
    def BuyStock(self, request, context):
        print(request.stock)
        reply = basics_pb2.TransactionSummary()
        reply.cost = 1000

        return reply


def serve():

    # The port you want to use
    port = "50051"
    
    # Instantiate the server with gRPC methods
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # To the server which we created, we need to add the class Greeter to the server
    basics_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    basics_pb2_grpc.add_StockBuyerServicer_to_server(StockBuyer(), server)

    # This is the port that we are going to use
    server.add_insecure_port("[::]:" + port)

    # Start the server
    server.start()
    print("Server started, listening on " + port)

    # Keep the server alive until terminations
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
