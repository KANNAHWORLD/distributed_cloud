import grpc
import os
import logging
import Terminal_pb2_grpc
import Terminal_pb2


class Terminal(Terminal_pb2_grpc.TerminalServicer):
    """
    A gRPC server implementation for a terminal service.

    This class provides methods to handle incoming gRPC requests related to the terminal functionality.
    """

    def ping(self, request, context):
        """
        Handles the ping request.

        Args:
            request: The ping request message.
            context: The gRPC context.

        Returns:
            The ping reply message.
        """
        logging.log(logging.INFO, "Recieved ping request")
        # print("Recieved ping request")
        reply = Terminal_pb2.PingReply()
        reply.message = "Pong"
        reply.alive = True
        reply.id = os.getpid()
        return reply
    
    # def SayHello(self, request, context):
    #     print(request.hello)
    #     reply = basics_pb2.HelloReply()
    #     reply.serverMessage = "Hello, Sid"
    #     reply.randomNumber = 100
        
    #     return reply