import os
import sys
import unittest
import requests

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from app import app, bcrypt, db # noqa
from app.models import User # noqa
from app.db import session # noqa
from app.db import create_db_tables # noqa


class UserUnitTest(unittest.TestCase):

    def setUp(self):
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def test_restricted_user_endpoints_without_auth(self):
        with self.app:
            response_users = requests.get('http://127.0.0.1:5000/api/v1/users')
            response_add_users = requests.post('http://127.0.0.1:5000/api/v1/users',
                                               data={'username': 'user1',
                                                     'email': 'user1@foo.com',
                                                     'password': '12345678'})
            response_delete_users = requests.delete('http://127.0.0.1:5000/api/v1/user/3')
            self.assertEqual(401, response_users.status_code)
            self.assertEqual(401, response_add_users.status_code)
            self.assertEqual(401, response_delete_users.status_code)

    def test_restricted_user_endpoints_with_auth(self):
        with self.app:
            user = session.query(User).get(1)
            response = requests.post('http://127.0.0.1:5000/api/v1/login', data={
                                     'email': user.email,
                                     'password': user.password})
            self.assertTrue(user.authenticated)
            response_users = requests.get('http://127.0.0.1:5000/api/v1/users')
            response_add_users = requests.post('http://127.0.0.1:5000/api/v1/users',
                                               data={'username': 'user1',
                                                     'email': 'user1@foo.com',
                                                     'password': '12345678'})
            response_delete_users = requests.delete('http://127.0.0.1:5000/api/v1/user/2')
            self.assertEqual(200, response.status_code)
            self.assertEqual(200, response_users.status_code)
            self.assertEqual(200, response_add_users.status_code)
            self.assertEqual(200, response_delete_users.status_code)

    def test_unauth(self):
        with self.app:
            user = session.query(User).get(1)
            self.assertFalse(user.authenticated)

    def test_login(self):
        with self.app:
            user = session.query(User).get(1)
            response = requests.post('http://127.0.0.1:5000/api/v1/login',
                                     data={'email': user.email,
                                           'password': user.password})
            self.assertTrue(user.authenticated)
            self.assertEqual(200, response.status_code)

    def test_logout(self):
        with self.app:
            # logging in
            user = session.query(User).get(1)
            response_login = requests.post('http://127.0.0.1:5000/api/v1/login',
                                           data={'email': user.email,
                                                 'password': user.password})
            self.assertEqual(200, response_login.status_code)
            self.assertTrue(user.authenticated)
            # logging out
            response_logout = self.app.post('http://127.0.0.1:5000/api/v1/logout')
            # assert that logout was made
            self.assertEqual(200, response_logout.status_code)

if __name__ == '__main__':
    unittest.main()
