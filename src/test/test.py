import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'back'))

# Import user and database modules
from model.user import user
from db.user_db import user_db 
from controller.user_bean import user_bean 

class TestUserBean(unittest.TestCase):

    test_user = None
    test_db = None

    def setUp(self):
        self.test_user = user('Tester', 'testing')
        self.test_db = user_db()

    def tearDown(self):
        '''
        remove any created objects
        '''
        self.test_user = None
        self.test_db = None

    def test_connect(self):
        u = user_bean()
        # test a successful connection
        self.assertTrue(u.connect('Tester', 'testing'))
        # test an unsuccessful connection
        self.assertFalse(u.connect('Wrong', 'Wrong'))

    def test_is_exist(self):
        u = user_bean()
        # test if a user exists
        expected = True
        actual = u.is_exist('Tester')
        self.assertEqual(expected, actual)
        # test if a user doesn't exist
        expected = False
        actual = u.is_exist('NonExistent')
        self.assertEqual(expected, actual)

    def test_destruct_user(self):
        u = user_bean(self.test_user.get_username(), self.test_user.get_password())
        u.destruct_user()
        self.assertEqual(u.get_user().get_id(), -1)

    def test_get_user_id(self):
        u = user_bean(self.test_user.get_username(), self.test_user.get_password())
        u = u.create_user(self.test_user)
        expected = u.get_user().get_id() + 1
        actual = u.get_user_id()
        self.assertEqual(expected, actual)

    def test_select_all(self):
        u = user_bean(self.test_user.get_username(), self.test_user.get_password())
        u.create_user(self.test_user)
        expected = [u.get_user()]
        actual = u.select_all()
        self.assertEqual(expected, actual)

    def test_get_user(self):
        u = user_bean(self.test_user.get_username(), self.test_user.get_password())
        u.create_user(self.test_user)
        expected = self.test_user
        actual = u.get_user(username=self.test_user.get_username())
        self.assertIsNotNone(actual)
        self.assertEqual(expected.get_username(), actual.get_username())
        self.assertEqual(expected.get_password(), actual.get_password())

    def test_create_user(self):
        u = user_bean(self.test_user.get_username(), self.test_user.get_password())
        u.create_user(self.test_user)
        self.assertNotEqual(u.get_user().get_id(), -1)
        
    def test_update_user(self):
        u = user_bean(self.test_user.get_username(), self.test_user.get_password())
        u.create_user(self.test_user)
        expected = 'newPassword'
        u.get_user().set_password(expected)
        u.update_user(u.get_user())
        actual = u.get_user().get_password()
        self.assertEqual(expected, actual)

    def test_delete_user(self):
        u = user_bean(self.test_user.get_username(), self.test_user.get_password())
        u.create_user(self.test_user)
        expected = False
        u.delete_user(u.get_user())
        actual = u.get_user(username=self.test_user.get_username())
        self.assertEqual(expected, actual)	

if __name__ == '__main__':
    unittest.main()