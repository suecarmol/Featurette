import sys
import os
import unittest
import requests

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app import app, bcrypt # noqa
from app.models import User, Client # noqa
from app.db import session # noqa
from app.db import create_db_tables # noqa


class ClientUnitTest(unittest.TestCase):

    def setUp(self):
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def test_restricted_client_endpoints_without_auth(self):
        response_clients = requests.get('http://127.0.0.1:5000/api/v1/clients')
        response_add_clients = requests.post('http://127.0.0.1:5000/api/v1/clients',
                                             data={'name': 'Test1'})
        response_delete_clients = requests.delete('http://127.0.0.1:5000/api/v1/client/2')
        self.assertEqual(401, response_clients.status_code)
        self.assertEqual(401, response_add_clients.status_code)
        self.assertEqual(401, response_delete_clients.status_code)

    def test_restricted_client_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash
                    ('12345678'))
        session.add(user)
        session.commit
        assert user in session
        response = requests.post('http://127.0.0.1:5000/api/v1/login', data={
                                 'email': user.email,
                                 'password': user.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue(user.authenticated)
        response_clients = requests.get('http://127.0.0.1:5000/api/v1/clients')
        response_add_clients = requests.post('http://127.0.0.1:5000/api/v1/clients',
                                             data={'name': 'Test1'})
        response_delete_clients = requests.delete('http://127.0.0.1:5000/api/v1/client/2')
        self.assertEqual(200, response_clients.status_code)
        self.assertEqual(200, response_add_clients.status_code)
        self.assertEqual(200, response_delete_clients.status_code)

    def test_add_client(self):
        response = requests.post('http://127.0.0.1:5000/api/v1/clients',
                                    {'name': 'Client BB8'})
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()
