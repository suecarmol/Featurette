import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..')) # noqa
from app import app
from config import config
from app.models import User
from app.db import session
from app.db import create_db_tables
from app.db import delete_db_tables


class UserUnitTest(unittest.TestCase):

    def setUp(self):
        # LOGIN_DISABLED flag is turned on
        app.config.from_object(config['test'])
        app.login_manager.init_app(app)
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def tearDown(self):
        app.test_mode = False
        delete_db_tables

    def test_get_all_users(self):
        with self.app:
            response_all_users = self.app.get('/api/v1/users')
            self.assertEqual(200, response_all_users.status_code)

    def test_get_one_user(self):
        with self.app:
            response_user = self.app.get('/api/v1/user/1')
            self.assertEqual(200, response_user.status_code)

    def test_add_user(self):
        with self.app:
            response_add_user = self.app.post('/api/v1/users',
                                              data={'username': 'user871',
                                                    'email': 'user871@foo.com',
                                                    'password': '12345678'})
            self.assertEqual(201, response_add_user.status_code)

    def test_edit_user(self):
        with self.app:
            response_edit_user = self.app.put('/api/v1/user/1',
                                              data={'username': 'editeduser',
                                                    'email': 'email@foo.com',
                                                    'password': '12345678'})
            self.assertEqual(201, response_edit_user.status_code)

    def test_delete_user(self):
        with self.app:
            response_delete_user = self.app.delete('/api/v1/user/2')
            self.assertEqual(200, response_delete_user.status_code)

    def test_unauth(self):
        with self.app:
            user = session.query(User).get(1)
            self.assertFalse(user.authenticated)

if __name__ == '__main__':
    unittest.main()
