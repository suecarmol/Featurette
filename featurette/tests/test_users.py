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
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = requests.post('http://127.0.0.1:5000/api/v1/login', data={
                                 'email': user.email,
                                 'password': user.password})
        self.assertEqual(200, response.status_code)
        logout = requests.post('http://127.0.0.1:5000/api/v1/logout')
        response_users = requests.get('http://127.0.0.1:5000/api/v1/users')
        response_add_users = requests.post('http://127.0.0.1:5000/api/v1/users',
                                           data={'username': 'user1',
                                                 'email': 'user1@foo.com',
                                                 'password': '12345678'})
        response_delete_users = requests.delete('http://127.0.0.1:5000/api/v1/user/3')
        self.assertEqual(200, logout.status_code)
        self.assertEqual(401, response_users.status_code)
        self.assertEqual(401, response_add_users.status_code)
        self.assertEqual(401, response_delete_users.status_code)

    def test_restricted_user_endpoints_with_auth(self):
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
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
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        self.assertFalse(user.authenticated)

    def test_login(self):
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = requests.post('http://127.0.0.1:5000/api/v1/login', data={
                                 'email': user.email,
                                 'password': user.password})
        self.assertEqual(200, response.status_code)
        self.assertEqual(user.username, 'username')
        self.assertTrue(user.authenticated)

    def test_logout(self):
        # logging in
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response_login = requests.post('http://127.0.0.1:5000/api/v1/login',
                                       data={'email': user.email,
                                             'password': user.password})
        self.assertEqual(200, response_login.status_code)
        self.assertTrue(user.authenticated)
        # logging out
        response_logout = self.client.get('/logout')
        # assert that logout was made
        self.assertEqual(200, response_logout.status_code)
        self.assertFalse(user.authenticated)


if __name__ == '__main__':
    unittest.main()
