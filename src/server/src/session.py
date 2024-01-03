import grpc
import threading
import filesys
import time
import uuid
import double_LL as dLL

class Session:

    # Used to store the state of each machine
    # Need to send session key with each request otherwise this won't work

    # After 10 minutes inactivity, the session times out
    TIME_OUT = 600

    def __init__(self, time_out: bool = True):
        
        self.sessionKey = uuid.uuid4() # Need to generate a token here

        # Keeping a filesystem object for each session
        # Initializing a new filesystem object for each session
        self.Filesys = filesys.Filesys()

        # Amount of time before the session times out, default is 10 minutes, if time_out is false, then the session never times out
        self.sessionTimeOut = (time.time() + self.TIME_OUT) if time_out else int("inf")
    
    def session_touch(self) -> None:
        """
        Extends the time a session is alive
        session was alive, extend session time
        """
        self.sessionTimeOut = time.time() + self.TIME_OUT
    
    def is_alive(self):
        return time.time() < self.sessionTimeOut

class SessionInterceptor(grpc.ServerInterceptor):
    
    # Dictionary of key_id to dLL node object
    IDSessionsNodes = {}

    # Double linked list of Node Objects, sorted by time
    SessionTime = dLL.DoubleLinkedList()
    sessionLock = threading.Lock()
    
    def intercept_service(self, func, handler_call_details):
        
        # Check if the metadata contains a session key
        # If it does, then check if the session is still alive
        metadata = dict(handler_call_details.invocation_metadata)
        # print(metadata)
        sessionID = None

        if sessionID in metadata:
            sessionID = metadata["session_id"]
        
        if sessionID in self.IDSessionsNodes:

            node = self.IDSessionsNodes[sessionID]
            
            if not node.is_alive():
                # If the session is not alive, then remove the session from the dictionary and the dLL
                self.IDSessionsNodes.pop(sessionID)
                self.SessionTime.remove_node(node)
                node = None
            else:
                # If the session is alive, then extend the session time
                node.data.session_touch()
        else:
            # If session ID is not in the dictionary, then node doesn't exist
            node = None

        if node is None:
            # Create a new session and add it to the metadata tab
            newSession = Session()
            node = self.SessionTime.create_add_node(newSession)
            self.IDSessionsNodes[newSession.sessionKey] = node


        new_handler_call_details = handler_call_details._replace(invocation_metadata=(tuple(metadata.items())))
        print(new_handler_call_details)

        return func(new_handler_call_details)
        


