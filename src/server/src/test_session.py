import unittest
import session
import time 

class TestSesssion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.sesion_verifier = session.SessionInterceptor()

    def test_create_session(self):

        # Create a new session
        newSession = self.sesion_verifier.create_session()
        
        # After creaeting a new session check if it is still alive
        self.assertTrue(newSession.is_alive())

        # After creating the session check if the session is in the dictionary
        self.assertTrue(newSession.sessionKey in self.sesion_verifier.IDSessionsNodes)

        # Check if the session is in the linked list
        DLL_node = self.sesion_verifier.IDSessionsNodes[newSession.sessionKey]
        self.assertTrue(DLL_node.data == newSession)

    def test_delete_session(self):
        
        # Create a new session
        newSession = self.sesion_verifier.create_session()

        # Delete the session
        self.sesion_verifier.delete_session(newSession.sessionKey)

        # Check if the session is still in the dictionary
        self.assertFalse(newSession.sessionKey in self.sesion_verifier.IDSessionsNodes)

        # Check if the session is still in the linked list, check if dLL head is None
        # print(self.sesion_verifier.SessionTime.head, self.sesion_verifier.SessionTime.tail)
        self.assertTrue(self.sesion_verifier.SessionTime.head == None and \
                        self.sesion_verifier.SessionTime.tail == None)

    def test_timed_out(self):

        # Create a new session
        newSession = self.sesion_verifier.create_session()
        newSession.sessionTimeOut = time.time()

        # Set the session to be timed out
        # Create a new session which should remove timed out sessions
        anotherNewSession = self.sesion_verifier.create_session()

        # Make sure old session was deleted
        self.assertTrue(self.sesion_verifier.number_of_sessions() == 1)

        # Check if the session is still in the dictionary
        self.assertTrue(anotherNewSession.sessionKey in self.sesion_verifier.IDSessionsNodes)

        # Check to make sure the linked list contain sessions
        self.assertFalse(self.sesion_verifier.SessionTime.head == None and \
                        self.sesion_verifier.SessionTime.tail == None)
        
        # Check to make sure there is only one session in the linked list
        self.assertTrue(self.sesion_verifier.SessionTime.head == self.sesion_verifier.SessionTime.tail)

    def test_session_touch(self):
            
            # Create a new session
            newSession = self.sesion_verifier.create_session()
    
            # Touch the session
            oldSessionTime = newSession.sessionTimeOut
            newSession.session_touch()
            self.assertTrue(oldSessionTime < newSession.sessionTimeOut)
    
            # Check if the session is still alive
            self.assertTrue(newSession.is_alive())
    
            # Check if the session is still in the dictionary
            self.assertTrue(newSession.sessionKey in self.sesion_verifier.IDSessionsNodes)
    
            # Check if the session is still in the linked list
            DLL_node = self.sesion_verifier.IDSessionsNodes[newSession.sessionKey]
            self.assertTrue(DLL_node.data == newSession)
    
    def test_get_session(self):
        # need to make sure that it is the same session
        # Creates a new session if session not found
        newSession = self.sesion_verifier.get_session('1')
        # print("Session created with key: ", newSession.sessionKey)
        self.assertTrue(newSession.sessionKey)

        # Create another new session
        newSession2 = self.sesion_verifier.get_session('1')
        # print("Session2 created with key: ", newSession.sessionKey)
        # make sure session IDs are not the same
        self.assertTrue(newSession.sessionKey != newSession2.sessionKey)
        self.assertTrue(newSession != newSession2)

        # Check if newSession2 is not the head of the DLL
        self.assertFalse(self.sesion_verifier.SessionTime.head.data == newSession2)

        # New session should be the tail of the DLL after creation
        newSession3 =  self.sesion_verifier.get_session("1")
        self.assertTrue(self.sesion_verifier.SessionTime.tail.data == newSession3)

        # if multiple sessions, if getting an old session it is bumped to the front of the queue
        newSession = self.sesion_verifier.get_session(newSession.sessionKey)
        self.assertTrue(self.sesion_verifier.SessionTime.tail.data == newSession)

    def test_multiple_delete_on_create(self):
        '''
        Tests if all sessions are removed when multiple sessions are timed out
        '''

        # Create a new session
        newSession = self.sesion_verifier.create_session()

        # Create another new session
        anotherNewSession = self.sesion_verifier.create_session()

        # Create another new session
        anotherNewSession2 = self.sesion_verifier.create_session()

        # Change timeOut times for all existing sessions
        newSession.sessionTimeOut = time.time()
        anotherNewSession.sessionTimeOut = time.time()
        anotherNewSession2.sessionTimeOut = time.time()

        # Create a new session which should remove timed out sessions
        anotherNewSession3 = self.sesion_verifier.create_session()

        # Check the data structures, no other sessions in the dictionary
        # only one session in the linked list, which would be the most recent one
        self.assertTrue(self.sesion_verifier.number_of_sessions() == 1)
        self.assertTrue(self.sesion_verifier.SessionTime.head.data == anotherNewSession3)
        self.assertTrue(self.sesion_verifier.SessionTime.tail.data == anotherNewSession3)

if __name__ == '__main__':
    unittest.main(verbosity=2)

    