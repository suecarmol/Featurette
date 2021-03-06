import os
import sys
import unittest

from flask import json

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..')) # noqa

from app import app
from config import config
from app.db import create_db_tables
from app.db import delete_db_tables


class ApiTest(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config['test'])
        app.login_manager.init_app(app)
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def tearDown(self):
        app.test_mode = False
        delete_db_tables

    def test_get_clients(self):
        with self.app:
            result = self.app.get('/api/v1/clients')
            data = json.loads(result.data)

            self.assertEqual(200, result.status_code)
            self.assertEqual(4, len(data))

            self.assertEqual(1, data[0]['id'])
            self.assertEqual('Client A', data[0]['name'])

    def test_get_users(self):
        with self.app:
            result = self.app.get('/api/v1/users')
            data = json.loads(result.data)

            self.assertEqual(200, result.status_code)
            self.assertEqual(6, len(data))

            self.assertEqual(2, data[1]['id'])
            self.assertEqual('username1', data[1]['username'])
            self.assertFalse(data[1]['authenticated'])
            self.assertFalse(data[1]['token'])
            self.assertTrue(data[1]['password'])
            self.assertEqual('username1@foo.com', data[1]['email'])

    def test_suggest_endpoint(self):
        with self.app:
            result = self.app.get('/api/v1/product_areas')
            data = json.loads(result.data)

            self.assertEqual(404, result.status_code)
            self.assertIn('did you mean /api/v1/productAreas', data['message'])

    def test_get_product_areas(self):
        with self.app:
            result = self.app.get('/api/v1/productAreas')
            data = json.loads(result.data)

            self.assertEqual(200, result.status_code)
            self.assertEqual(4, len(data))

            self.assertEqual(1, data[0]['id'])
            self.assertEqual('Policies', data[0]['name'])

    def test_get_feature_requests(self):
        with self.app:
            result = self.app.get('/api/v1/featureRequests')

            self.assertEqual(200, result.status_code)
            data = json.loads(result.data)
            print data


if __name__ == '__main__':
    unittest.main()
