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
        reply = Terminal_pb2.TerminalOutput(output="Pong", alive=True)
        return reply
    

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
    file_delimiter = chr(29)
    file_name_delimiter = chr(30)
    # Actual directory on the server machine
    absolute_path = os.getcwd()+"/sharedDirec/."

    # relative directory for the user connected to the server
    
    # This is the root directory of the server
    root_directory = '~'

    # Default root directory for the server
    user_directory = root_directory

    # list of files in the current directory
    # User contains just file and that data
    user_loaded_directory = []
    # Contains all raw data such as ip+port+permissions of the server which contains the file
    private_loaded_directory = []

    def load_directory(self, directory):
        """
        Loads the directory from the server machine into the server memory.
        """
        file = open(directory, 'r')
        self.private_loaded_directory = [line.split(self.file_delimiter) for line in file]
        file.close()

        # Capturing only the filenames from the private_loaded_directory
        self.user_loaded_directory = [entry[0] for entry in self.private_loaded_directory]

        return

    # TODO need to add support of permissions for files
    # Need to keep track of which machines has which files
    def cd(self, request, context):
        """
        Change the current directory.

        Args:
            request: The request object containing the directory to change into.
            context: The context object for the gRPC request.

        Returns:
            A response object containing the new current directory path.

        Raises:
            None
        """
        
        req_direc = request.path

        #Maybe check if the requested directory contains the file name delimiter

        if req_direc == '..':
            # User is trying to exit the current directory
            # Check if the user is in the root directory
            if self.user_directory == self.root_directory:
                # User is in the root directory
                # Send error message to user
                return Terminal_pb2.TerminalOutput(pwd=self.user_directory)
            else:
                # User is not in the root directory
                # Remove the last directory from the user directory
                self.user_directory = self.user_directory[:self.user_directory.rindex(self.file_name_delimiter)]
        elif req_direc in self.user_loaded_directory:
            index = self.user_loaded_directory.index(req_direc)
            if self.private_loaded_directory[index][1] == 'D':
                # User is trying to change into a directory
                # Change the user directory
                self.user_directory += self.file_name_delimiter + req_direc
            else:
                # In case you are trying to change into a file
                return Terminal_pb2.TerminalOutput(pwd=self.user_directory)
        else:
            return Terminal_pb2.TerminalOutput(pwd=self.user_directory)

        # Loading in the new directory if the directory needs to be changed
        self.load_directory(self.absolute_path+self.user_directory)
        # print(self.user_loaded_directory, self.private_loaded_directory)
        return Terminal_pb2.TerminalOutput(pwd=self.user_directory)

        # cases to test for:
            # User exiting directory beyond root directory # Done
            # User chaning into a non existent directory # Done
            # User changing into a directory that is a file # Done
        
    def ls(self, request, context):
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
        reply = Terminal_pb2.TerminalOutput\
            (output="\n".join(self.user_loaded_directory), pwd=self.user_directory, alive=True)
        return reply

    def pwd(self, request, context):
        """
        Print the current directory.

        Args:
            request: The request object containing the directory to change into.
            context: The context object for the gRPC request.

        Returns:
            A response object containing the current directory.

        Raises:
        """
        return Terminal_pb2.TerminalOutput(pwd=self.user_directory)
    
    def mkdir(self, request, context):
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
        path_creation = request.path
        # Check if the directory already exists
