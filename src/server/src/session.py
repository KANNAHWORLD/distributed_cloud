import threading
import filesys
import time
import uuid
import double_LL as dLL

class Session:
    """
    Represents a session for a machine.

    Attributes:
        sessionKey (uuid.UUID): The unique session key generated for the session.
        Filesys (filesys.Filesys): The filesystem object associated with the session.
        sessionTimeOut (float): The timestamp indicating when the session will time out.
    """

    TIME_OUT = 600

    def __init__(self, time_out: bool = True):
        """
        Initializes a new session.

        Args:
            time_out (bool, optional): Determines if the session should time out after a period of inactivity. Defaults to True.
        """
        self.sessionKey = uuid.uuid4()
        self.Filesys = filesys.Filesys()
        self.sessionTimeOut = (time.time() + self.TIME_OUT) if time_out else float("inf")
    
    def session_touch(self) -> None:
        """
        Extends the time a session is alive.
        """
        self.sessionTimeOut = time.time() + self.TIME_OUT
    
    def is_alive(self) -> bool:
        """
        Checks if the session is still alive.

        Returns:
            bool: True if the session is alive, False otherwise.
        """
        return time.time() < self.sessionTimeOut

class SessionInterceptor():

    def __init__(self) -> None:
        """
        Initializes a new session interceptor.
        """
        # Dictionary of key_id to dLL node object
        self.IDSessionsNodes = {}

        # Double linked list of Node Objects, sorted by time
        self.SessionTime = dLL.DoubleLinkedList()
        self.sessionLock = threading.Lock()
    
    def get_session(self, sessionID) -> Session:
        """
        Retrieves a session based on the provided metadata.
        If a session with the given session ID exists and is still alive, it is returned.
        Otherwise, a new session is created.

        Args:
            sessionID (str): The session ID to retrieve the state for.

        Returns:
            Session: The retrieved or newly created session.
        """

        # Remove all timed out sessions
        self.helper_remove_timed_out_sessions()

        if sessionID in self.IDSessionsNodes:

            node = self.IDSessionsNodes[sessionID]
            self.sessionLock.acquire()
            if not node.data.is_alive():
                # If session is not alive, then delete the session
                self.helper_nolock_delete_session(sessionID)
                node = None
            else:
                # If the session is alive, then extend the session time
                node.data.session_touch()
                # Move node to the end of the dLL since it is terminating later
                self.SessionTime.move_to_end(node)
                # So you can return the session object
                node = node.data
            self.sessionLock.release()
        else:
            # If session ID is not in the dictionary, then node doesn't exist
            node = None

        if node is None:
            # If the session doesn't exist, then create a new session
            node = self.create_session()

        return node
        
    def create_session(self) -> Session:
        """
        Creates a new session and adds it to the session dictionary and the session dLL
        """
        self.helper_remove_timed_out_sessions()
        
        self.sessionLock.acquire()
        newSession = Session()
        node = self.SessionTime.create_add_node(newSession)
        self.IDSessionsNodes[newSession.sessionKey] = node
        self.sessionLock.release()
        return newSession

    def delete_session(self, session_id) -> None:
        """
        Deletes a session from the session dictionary and the session dLL
        """
        self.sessionLock.acquire()
        self.helper_nolock_delete_session(session_id)
        self.sessionLock.release()
        return

    def number_of_sessions(self) -> int:
        """
        Returns the number of sessions in the session dictionary
        """
        return len(self.IDSessionsNodes)

    # Helper functions, do not call these functions outside of the class
    def helper_nolock_delete_session(self, session_id) -> None:
        """
        Deletes a session from the session dictionary and the session dLL
        """
        node = self.IDSessionsNodes[session_id]
        self.SessionTime.remove_node(node)
        self.IDSessionsNodes.pop(session_id)
        return

    def helper_remove_timed_out_sessions(self) -> None:
        """
        Removes all timed out sessions from the session dictionary and the session dLL
        """
        self.sessionLock.acquire()
        # Remove all timed out sessions
        session = self.SessionTime.get_front()
        while session:
            # DLL is sorted earliest terminating in the front
            if not session.is_alive():
                self.helper_nolock_delete_session(session.sessionKey)
            else:
                break
            session = self.SessionTime.get_front()
        self.sessionLock.release()
        return

