import unittest
from filesys import Filesys

class TestFilesys(unittest.TestCase):
    
    def setUp(self):

        # Create a new file system
        self.fs = Filesys()

    def test1(self):
        self.assertTrue(True)
        pass