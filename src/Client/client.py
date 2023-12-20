

from __future__ import print_function

import logging

import grpc
import basics_pb2_grpc
import basics_pb2


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = basics_pb2_grpc.GreeterStub(channel)
        stockStub = basics_pb2_grpc.StockBuyerStub(channel)
        response = stub.SayHello(basics_pb2.HelloRequest(date = 32))
        stockResponse = stockStub.BuyStock(basics_pb2.BuyRequest(quantity=100, id=1, stock="AAPL"))
        print(stockResponse.cost)
    print("Greeter client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run()
