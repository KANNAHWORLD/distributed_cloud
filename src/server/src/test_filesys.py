import unittest
import os
import shutil
from filesys import Filesys

class TestFilesys(unittest.TestCase):
    

    def setUp(self):
        # Create a new file system
        self.fs = Filesys()

    def tearDown(self) -> None:
        
        # DO NOT CHANGE this, it can delete entire laptop
        tearDownPath = os.getcwd() + "/unittest/"
        #########################################

        # print(tearDownPath)
        # shutil.rmtree(tearDownPath)

    def test_constructor(self):
        self.assertTrue(os.path.exists(self.fs.absolute_path))
        self.assertTrue(os.path.exists(self.fs.absolute_path+'.1'))

    def test_pwd(self):
        self.assertTrue(self.fs.pwd() == "~")

        
if __name__ == '__main__':
    # Changing static variable to modify the root directory
    # for unittestPurposes
    Filesys.absolute_path = os.getcwd() + "/unittest/sharedDirec/"
    unittest.main(verbosity=2)