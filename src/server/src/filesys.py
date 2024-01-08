import os
import logging
import asyncio
import threading


class Filesys():
    fileSystemLock = threading.Lock()
    fileSystemUpdate = threading.Condition()
    
    # Constants
    file_content_delimiter = chr(29)
    file_name_delimiter = chr(30)
    # Actual directory on the server machine

    # TODO: this eventually needs to change such that the shared directory is not in 
    # the same directory as the server src
    absolute_path = os.getcwd()+"/sharedDirec/"

    # File numbers, each file is stored as a file number in the server
    # TODO: figure out a way in case there is number overflow
    nextFileNumber = 2   


    def __init__(self) -> None:
        """
        Initializes an instance of the Filesys class.
        
        Instance Variables:
        - number_directory_stack: A stack of directory numbers representing the user's traversal history.
        - name_user_directory: A list representing the current directory path.
        - user_loaded_directory: A list of files in the current directory.
        - private_loaded_directory: A list of raw data such as IP, port, and permissions of the server which contains the file.
        """

        # New directory by numbers
        self.number_directory_stack = ['1']

        # Default root directory for the server
        self.name_user_directory = ["~"]

        # Creates the initial sharedDirec folder
        if not os.path.exists(self.absolute_path):
            os.makedirs(self.absolute_path)
            
        # This creates the initial root directory
        if not os.path.exists(self.folder_path(self.number_directory_stack[-1])):
            open(self.folder_path(self.number_directory_stack[-1]), 'w').close()

        # list of files in the current directory
        # User contains just file and that data
        self.user_loaded_directory = []

        # Contains all raw data such as IP, port, and permissions of the server which contains the file
        self.private_loaded_directory = []
        self.load_directory(self.number_directory_stack[-1])

    def load_directory(self, directory) -> None:
        """
        Loads the directory from the server machine into the server memory.
        Loads it into self.private_loaded_directory and self.user_loaded_directory.

        Args:
            directory (str): The name of the directory to be loaded.

        Returns:
            None
        """
        file = open(self.folder_path(directory), 'r')
        self.private_loaded_directory = [line.split(self.file_content_delimiter) for line in file]
        file.close()

        # Capturing only the filenames from the private_loaded_directory
        self.user_loaded_directory = [self.file_name(entry) for entry in self.private_loaded_directory]
        return

    # TODO need to add support of permissions for files
    # Need to keep track of which machines has which files
    # Rest of the code...
    def cd(self, path: str) -> str:
        """
        Change the current directory to the specified path.

        Args:
            path (str): The path of the directory to change into.

        Returns:
            str: The updated current directory path.

        Raises:
            None

        Examples:
            >>> fs = FileSystem()
            >>> fs.cd('dir1')
            '/dir1'
            >>> fs.cd('..')
            '/'
            >>> fs.cd('file1')
            '/'
        """
        
        self.fileSystemLock.acquire()
        self.helper_cd(path)
        self.fileSystemLock.release()
    
        return self.pwd()

    def folder_path(self, path: str) -> str:
        """
        Returns the absolute path of the specified path.

        Args:
            path (str): The path to get the absolute path of.

        Returns:
            str: The absolute path of the specified path.

        Raises:
            None
        """
        return self.absolute_path + '.' + path

    def file_path(self, path: str) -> str:
        """
        Returns the absolute path of the specified path.

        Args:
            path (str): The path to get the absolute path of.

        Returns:
            str: The absolute path of the specified path.

        Raises:
            None
        """

        # creates the absolute path of a local file
        return self.absolute_path + self.pwd()[2:] + '/' + path

    def is_directory(self, entry: list) -> bool:
        """
        Checks if the path is a directory.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path is a directory, False otherwise.

        Raises:
            None
        """
        return entry[2] == 'D'

    def file_name(self, entry: list) -> str:
        """
        Returns the file name from the path.

        Args:
            path (str): The path to check.

        Returns:
            str: The file name.

        Raises:
            None
        """
        return entry[1]

    def file_number(self, entry: list) -> str:
        """
        Returns the file number from the path.

        Args:
            path (str): The path to check.

        Returns:
            str: The file number.

        Raises:
            None
        """
        return entry[0]

    def local_folder_path(self, path: str) -> str:
        """
        Returns the absolute path for creating a local folder path.

        Args:
            path (str): The path to get the absolute path of.

        Returns:
            str: The absolute path of the specified path.

        Raises:
            None
        """
        return self.absolute_path + path[2:]

    def helper_cd(self, path: str) -> None:
        """
        Change the current directory to the specified path.

        Args:
            path (str): The path of the directory to change into.

        Returns:
            str: The updated current directory path.

        Raises:
            None

        Examples:
            >>> fs = FileSystem()
            >>> fs.cd('dir1')
            '/dir1'
            >>> fs.cd('..')
            '/'
            >>> fs.cd('file1')
            '/'
        """
        # Maybe check if the requested directory contains the file name delimiter

        if path == '..':
            # User is trying to exit the current directory
            # Check if the user is in the root directory
            if self.number_directory_stack[-1] == '1':
                # User is in the root directory
                return
            else:
                # User is not in the root directory
                # Remove the last directory from the user directory
                self.number_directory_stack.pop()
                self.name_user_directory.pop()

        elif path in self.user_loaded_directory:
            index = self.user_loaded_directory.index(path)
            if self.is_directory(self.private_loaded_directory[index]):
                # User is trying to change into a directory
                # Change the user directory
                self.name_user_directory.append(self.file_name(self.private_loaded_directory[index]))
                
                #appending the file number to the stack
                self.number_directory_stack.append(self.file_number(self.private_loaded_directory[index]))
            else:
                # In case you are trying to change into a file, just do nothing
                return 
        else:
            # User is trying to change into a directory that does not exist
            return

        # Loading in the new directory if the directory needs to be changed
        # TODO: Make sure you are calling this correctlys
        self.load_directory(self.number_directory_stack[-1])
        return

    def ls(self) -> str:
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

        return '\n'.join(self.user_loaded_directory)

    def pwd(self) -> str:
        """
        Print the current directory.

        Args:
            request: The request object containing the directory to change into.
            context: The context object for the gRPC request.

        Returns:
            A response object containing the current directory.

        Raises:
        """
        return '/'.join(self.name_user_directory)

    # TODO need to add support for permissions
    # TODO: need to update for new filesystme paradigm
    def rm(self, path) -> None:
        """
        Removes a file or directory from the server filesystem.

        Args:
            path (str): The path of the file or directory to remove.

        Returns:
            str: The updated current directory path.

        Raises:
            None

        Examples:
            >>> fs = FileSystem()
            >>> fs.rm('dir1')
            '/dir1'
            >>> fs.rm('..')
            '/'
            >>> fs.rm('file1')
            '/'

        """

        # Check permission of current folder

        # Recursively removes all files in subdirectories
        # TODO need to add support for permissions
        def helper_recursive_remove(path):        
            


            for subDir in self.private_loaded_directory:
                if subDir[1] == "D":
                    self.helper_cd(subDir[0])
                    helper_recursive_remove(self.name_user_directory)
                    self.helper_cd('..')

                    # Removing the metadata file
                    os.remove(self.absolute_path+self.name_user_directory+self.file_name_delimiter+subDir[0])
                else:
                    abs_file = self.absolute_path + self.pwd()+'/'+subDir[0]
                    
                    # If the file is found on this system, then you want to remove it
                    if os.path.exists(abs_file):
                        os.remove(abs_file)

        
        self.fileSystemLock.acquire()
        
        self.helper_cd(path)
        helper_recursive_remove(self.name_user_directory)
        self.private_loaded_directory.remove(path)
        self.updatePathMetadata()

        self.fileSystemLock.release()

    def update_path_metadata(self) -> None:
        """
        Opens a file and outputs the private loaded directory to the file.

        This function opens a file specified by the `self.absolute_path` and `self.name_user_directory` attributes,
        and writes the contents of the `self.private_loaded_directory` list to the file. Each entry in the list
        is joined using the `self.file_content_delimiter` delimiter.

        Note: Make sure to close the file after writing.

        Args:
            None

        Returns:
            None
        """
        file = open(self.folder_path(self.number_directory_stack[-1]), 'w')

        for entry in self.private_loaded_directory:
            print(self.file_content_delimiter.join(entry), file=file)

        file.close()
        return

    # internal function
    # TODO: Need to create new files for each new directory,
    # TODO: need to add support for permissions

    # TODO: Permissions, look into how to implement permissions, look into version control, using locks
    # TODO: Need to change th functionality depending on file or directory
    # TODO: check if an actual local file needs to be created
    # Return values 
    def createFile(self, name, DorF="D", node_registry='0', permissions="0") -> None:
        """
        Creates a path name by concatenating the provided parameters with the file content delimiter.
        TODO:
            Check if files names are illegal such as containing the file content delimiter or newline, (back) slash

        Args:
            name (str): The name of the file or directory.
            DorF (str): Indicates whether the path represents a file or directory.
            TODO: Check for zero
            node_registry (str): The node registry information. A value of '0' indicates that the folder/file will be created locally on the central server.
            permissions (str): The permissions for the path.

        Returns:
            None
        """
        if name in self.user_loaded_directory:
            return self.pwd()

        self.fileSystemUpdate.acquire()

        # Here chekc if there were any updates to the filesystem before creating the path
        file_number = str(self.nextFileNumber)
        self.nextFileNumber += 1

        self.private_loaded_directory.append([str(file_number), name, DorF, node_registry, permissions])
        self.user_loaded_directory.append(name)

        # Updating the metadata file by writing private_loaded_directory to the file
        self.update_path_metadata()
        
        if DorF == "D":
            open(self.folder_path(file_number), 'w').close()
        else:

            # TODO: check if the actula file actually needs to be created. 
            try:
                os.makedirs(self.local_folder_path(self.pwd()))
            except FileExistsError:
                pass
            except:
                pass
            
            open(self.file_path(name), 'w').close()

        self.fileSystemUpdate.release()

        return