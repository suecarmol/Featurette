import sys
import os
import unittest
import requests

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..')) # noqa
from app import app
from config import config
from app.models import User
from app.db import session
from app.db import create_db_tables
from app.db import delete_db_tables


class ClientUnitTest(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config['test'])
        app.login_manager.init_app(app)
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def tearDown(self):
        app.test_mode = False
        delete_db_tables

    def test_restricted_client_endpoints_without_auth(self):
        with self.app:
            response_clients = requests.get('http://127.0.0.1:5000/api/v1/clients')
            response_add_clients = requests.post('http://127.0.0.1:5000/api/v1/clients',
                                                 data={'name': 'Test1'})
            response_delete_clients = requests.delete('http://127.0.0.1:5000/api/v1/client/2')
            self.assertEqual(401, response_clients.status_code)
            self.assertEqual(401, response_add_clients.status_code)
            self.assertEqual(401, response_delete_clients.status_code)

    def test_restricted_client_endpoints_with_auth(self):
        with self.app:
            user = session.query(User).get(1)
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
        with self.app:
            response = requests.post('http://127.0.0.1:5000/api/v1/clients',
                                        {'name': 'Client BB8'})
            self.assertEqual(401, response.status_code)

if __name__ == '__main__':
    unittest.main()
