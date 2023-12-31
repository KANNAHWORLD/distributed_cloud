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

    # relative directory for the user connected to the server
    # This is the root directory of the server filesystem
    # Filesystem is implemented by a files with a filesystem name
    root_directory = '.~'

    # File numbers, each file is stored as a file number in the server
    



    def __init__(self) -> None:
        """
        Initializes an instance of the Filesys class.
        
        Instance Variables:
        - user_directory: The default root directory for the server.
        - user_loaded_directory: A list of files in the current directory.
        - private_loaded_directory: A list of raw data such as ip, port, and permissions of the server which contains the file.
        """
        
        # TODO: need to check if root directory file exists, if not create it

        # Default root directory for the server
        self.user_directory = self.root_directory

        # list of files in the current directory
        # User contains just file and that data
        self.user_loaded_directory = []
        # Contains all raw data such as ip+port+permissions of the server which contains the file
        self.private_loaded_directory = []
        self.load_directory(self.absolute_path+self.user_directory)

    def load_directory(self, directory):
        """
        Loads the directory from the server machine into the server memory.
        """
        file = open(directory, 'r')
        self.private_loaded_directory = [line.split(self.file_content_delimiter) for line in file]
        file.close()

        # Capturing only the filenames from the private_loaded_directory
        self.user_loaded_directory = [entry[0] for entry in self.private_loaded_directory]
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
    
        return self.user_directory.replace(self.file_name_delimiter, '/')
        
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
        req_direc = path

        # Maybe check if the requested directory contains the file name delimiter

        if req_direc == '..':
            # User is trying to exit the current directory
            # Check if the user is in the root directory
            if self.user_directory == self.root_directory:
                # User is in the root directory
                # Send error message to user
                return
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
                # In case you are trying to change into a file, just do nothing
                return 
        else:
            return

        # Loading in the new directory if the directory needs to be changed
        self.load_directory(self.absolute_path+self.user_directory)
        
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
        return self.user_directory.replace(self.file_name_delimiter, '/')[1:]

    # TODO need to add support for permissions
    def rm(self, path) -> str:
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
                    helper_recursive_remove(self.user_directory)
                    self.helper_cd('..')

                    # Removing the metadata file
                    os.remove(self.absolute_path+self.user_directory+self.file_name_delimiter+subDir[0])
                else:
                    abs_file = self.absolute_path + self.pwd()+'/'+subDir[0]
                    
                    # If the file is found on this system, then you want to remove it
                    if os.path.exists(abs_file):
                        os.remove(abs_file)

        
        self.fileSystemLock.acquire()
        
        self.helper_cd(path)
        helper_recursive_remove(self.user_directory)
        self.private_loaded_directory.remove(path)
        self.updatePathMetadata()

        self.fileSystemLock.release()

    def update_path_metadata(self):
        """
        Opens a file and outputs the private loaded directory to the file.

        This function opens a file specified by the `self.absolute_path` and `self.user_directory` attributes,
        and writes the contents of the `self.private_loaded_directory` list to the file. Each entry in the list
        is joined using the `self.file_content_delimiter` delimiter.

        Note: Make sure to close the file after writing.

        Args:
            None

        Returns:
            None
        """
        file = open(self.absolute_path+self.user_directory, 'w')

        for entry in self.private_loaded_directory:
            print(self.file_content_delimiter.join(entry), file=file)

        file.close()
        pass

    # internal function
    # TODO: Need to create new files for each new directory,
    # TODO need to add support for permissions
    # Check if the directory already exists

    # If directory already exists, do nothing, send message appropriately

    # If directory does not exist, create the directory # For permissions make sure to leave flxibility
    # For later

    # TODO: Permissions, look into how to implement permissions, look into version control, using locks
    
    # TODO: Need to return appropriate message if createPath worked or not 
    # Return values 
    def createFile(self, name, DorF="D", node_registry='0', permissions="0") -> None:
        """
        Creates a path name by concatenating the provided parameters with the file content delimiter.
        TODO:
            Check if files names are illegal such as containing the file content delimiter or newline, (back) slash

        Args:
            name (str): The name of the file or directory.
            DorF (str): Indicates whether the path represents a file or directory.
            node_registry (str): The node registry information.
            permissions (str): The permissions for the path.

        Returns:
            str: The concatenated path name.
        """
        if name in self.user_loaded_directory:
            return self.pwd()

        self.fileSystemUpdate.acquire()

        # Here chekc if there were any updates to the filesystem before creating the path

        self.private_loaded_directory.append([name, DorF, node_registry, permissions])
        self.private_loaded_directory.sort(key=lambda x: x[0])

        # Need to acquire lock
        # Need to notify other threads and nodes that directory has been updated

        # Updating the metadata file by writing private_loaded_directory to the file
        self.update_path_metadata()
        
        file = open(self.absolute_path+self.user_directory+self.file_name_delimiter+name, 'w')
        file.close()

        self.load_directory(self.absolute_path+self.user_directory)

        self.fileSystemUpdate.release()


