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
    
    def intercept_service(self, continuation, handler_call_details):
        
        # # Check if the metadata contains a session key
        # # If it does, then check if the session is still alive
        # sessionID = handler_call_details.invocation_metadata['session']
        # if sessionID in self.IDSessionsNodes:

        #     node = self.IDSessionsNodes[sessionID]
        #     if not node.is_alive():
        #         # If the session is alive, then update the time
        #         self.IDSessionsNodes.pop(sessionID)
        #         self.SessionTime.remove_node(node)
        #         return 
        #     # If the session is alive, then update the time
        #     node.data.session_touch()
            
        #     # If the session is not alive, then prompt the user to create a new session
            

        # If no key prompt the user to create a new session

        # handler_call_details.invocation_metadata.append(('session', ))

        # print(handler_call_details.invocation_metadata)
        # print(handler_call_details)
        response = continuation(handler_call_details)
        print(continuation)

        return response



