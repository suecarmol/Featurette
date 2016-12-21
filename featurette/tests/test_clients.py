import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..')) # noqa
from app import app
from config import config
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

    def test_get_all_clients(self):
        with self.app:
            response_all_clients = self.app.get('/api/v1/clients')
            self.assertEqual(200, response_all_clients.status_code)

    def test_get_one_client(self):
        with self.app:
            response_one_client = self.app.get('/api/v1/client/1')
            self.assertEqual(200, response_one_client.status_code)

    def test_add_client(self):
        with self.app:
            response_add_client = self.app.post('/api/v1/clients',
                                                data={'name': 'Test Client'})
            self.assertEqual(201, response_add_client.status_code)

    def test_edit_client(self):
        with self.app:
            response_edit_client = self.app.put('/api/v1/client/2',
                                                data={'name': 'Edited Client'})
            self.assertEqual(201, response_edit_client.status_code)

    def test_delete_client(self):
        with self.app:
            response_delete_client = self.app.delete('/api/v1/client/2')
            self.assertEqual(200, response_delete_client.status_code)

if __name__ == '__main__':
    unittest.main()
