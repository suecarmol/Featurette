import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..')) # noqa
from app import app
from app.models import User
from app.db import session
from app.db import create_db_tables
from app.db import delete_db_tables


class UserUnitTest(unittest.TestCase):

    def setUp(self):
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def tearDown(self):
        app.test_mode = False
        delete_db_tables

    def test_restricted_user_endpoints_without_auth(self):
        with self.app:
            response_users = self.app.get('/api/v1/users')
            response_add_users = self.app.post('/api/v1/users',
                                               data={'username': 'user1',
                                                     'email': 'user1@foo.com',
                                                     'password': '12345678'})
            response_delete_users = self.app.delete('/api/v1/user/3')
            self.assertEqual(401, response_users.status_code)
            self.assertEqual(401, response_add_users.status_code)
            self.assertEqual(401, response_delete_users.status_code)

    def test_restricted_user_endpoints_with_auth(self):
        with self.app:
            user = session.query(User).get(1)
            response = self.app.post('/api/v1/login', data={
                                     'email': user.email,
                                     'password': user.password})
            self.assertTrue(user.authenticated)
            response_add_users = self.app.post('/api/v1/users',
                                               data={'username': 'user1',
                                                     'email': 'user1@foo.com',
                                                     'password': '12345678'})
            response_delete_users = self.app.delete('/api/v1/user/2')

            self.assertEqual(200, response.status_code)
            self.assertEqual(200, response_add_users.status_code)
            self.assertEqual(200, response_delete_users.status_code)

    def test_unauth(self):
        with self.app:
            user = session.query(User).get(4)
            self.assertFalse(user.authenticated)

    def test_login(self):
        with self.app:
            user = session.query(User).get(1)
            response = self.app.post('/api/v1/login',
                                     data={'email': user.email,
                                           'password': user.password})
            self.assertTrue(user.authenticated)
            self.assertEqual(200, response.status_code)

    def test_logout(self):
        user = session.query(User).get(1)
        with self.app as c:
            response_login = c.post('/api/v1/login', method='POST',
                                    data={'email': user.email,
                                          'password': user.password})
            self.assertTrue(user.authenticated)
            self.assertEqual(200, response_login.status_code)
            # logging out
            response_logout = c.post('/api/v1/logout')
            # assert that logout was made
            self.assertEqual(204, response_logout.status_code)

if __name__ == '__main__':
    unittest.main()
