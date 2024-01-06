import unittest
import session
import time 

class TestSesssion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sesion_verifier = session.SessionInterceptor()

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
        
        self.sesion_verifier = session.SessionInterceptor()
        
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

        # Create a new session_verifier
        self.sesion_verifier = session.SessionInterceptor()

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


if __name__ == '__main__':
    unittest.main(verbosity=2)