import grpc
import os
import logging
import asyncio
import threading

import Terminal_pb2_grpc
import Terminal_pb2
from filesys import Filesys


class Terminal(Terminal_pb2_grpc.TerminalServicer):
    """
    A gRPC server implementation for a terminal service.

    This class provides methods to handle incoming gRPC requests related to the terminal functionality.
    """
    '''
    # Distributed file system exists in such a way that 
    # current directory file which lists all files contained in the directory
    # also contains a list of all folders which can be found
    # File contains ip+port of the server which contains the file,
    # Each server contains its own shared directory which would can be searched by central server
    
    # directory File format such that 
    # 1. Directory path is filename
    # 2. each line in file contains file+folder data
    # 3. for file, file_name+file_or_directory+node_registry+permissions
    
    # D is for directory, F is file in second 

    # ASCII Delimiter Group separator
    '''
    
    def __init__(self) -> None:
        """
        Initializes an instance of the Terminal class.
        
        Instance Variables:
        - user_directory: The default root directory for the server.
        - user_loaded_directory: A list of files in the current directory.
        - private_loaded_directory: A list of raw data such as ip, port, and permissions of the server which contains the file.
        """

        self.fs = Filesys()
        pass

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
        reply = Terminal_pb2.TerminalOutput(output="Pong", alive=True)
        return reply

    # TODO need to add support of permissions for files
    # Need to keep track of which machines has which files
    def cd(self, request, context) -> Terminal_pb2.TerminalOutput:

        
        return Terminal_pb2.TerminalOutput(pwd=self.fs.cd(request.path))

        # cases to test for:
            # User exiting directory beyond root directory # Done
            # User chaning into a non existent directory # Done
            # User changing into a directory that is a file # Done

    def ls(self, request, context) -> Terminal_pb2.TerminalOutput:
        # TODO need to add support for permissions
        """
        List the contents of the current directory.

        Args:
            request: The request object containing the directory to change into.
            context: The context object for the gRPC request.

        Returns:
            A response object containing the contents of the current directory.

        Raises:
        """
        
        # Future add permissions here
        return Terminal_pb2.TerminalOutput(output=self.fs.ls(), alive=True)

    def pwd(self, request, context) -> Terminal_pb2.TerminalOutput:
        """
        Print the current directory.

        Args:
            request: The request object containing the directory to change into.
            context: The context object for the gRPC request.

        Returns:
            A response object containing the current directory.

        Raises:
        """
        return Terminal_pb2.TerminalOutput(pwd=self.fs.pwd())

    def mkdir(self, request, context) -> Terminal_pb2.TerminalOutput:
        """
        Create a new directory.

        Args:
            request: The request object containing the directory to change into.
            context: The context object for the gRPC request.

        Returns:
            A response object containing the current directory.

        Raises:
        """
        # TODO need to add support for permissions
        # Check if the directory already exists

        # If directory already exists, do nothing, send message appropriately

        # If directory does not exist, create the directory # For permissions make sure to leave flxibility
        # For later

        # TODO: Permissions, look into how to implement permissions, look into version control, using locks
        
        # TODO: Need to return appropriate message if createPath worked or not 
        # Return values

        metadata = dict(context.invocation_metadata())

        return Terminal_pb2.TerminalOutput(pwd=self.fs.createFile(request.path))

