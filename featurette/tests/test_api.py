import os
import sys
import unittest

from flask import json

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..')) # noqa

from app import app
from app.db import create_db_tables
from app.db import delete_db_tables


class ApiTest(unittest.TestCase):

    def setUp(self):
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def tearDown(self):
        app.test_mode = False
        delete_db_tables

    def test_get_clients(self):
        with self.app:
            login = self.app.post('/api/v1/login', data={'email': 'username@foo.com',
                                  'password': '12345678'})
            result = self.app.get('/api/v1/clients')
            data = json.loads(result.data)

            self.assertEqual(200, login.status_code)
            self.assertEqual(200, result.status_code)
            self.assertEqual(4, len(data))

            self.assertEqual(1, data[0]['id'])
            self.assertEqual('Client A', data[0]['name'])

            self.assertEqual(2, data[1]['id'])
            self.assertEqual('Client B', data[1]['name'])

            self.assertEqual(3, data[2]['id'])
            self.assertEqual('Client C', data[2]['name'])

            self.assertEqual(4, data[3]['id'])
            self.assertEqual('Client D', data[3]['name'])

    def test_get_users(self):
        with self.app:
            login = self.app.post('/api/v1/login', data={'email': 'username1@foo.com',
                                  'password': '12345678'})
            result = self.app.get('/api/v1/users')
            data = json.loads(result.data)

            self.assertEqual(200, login.status_code)
            self.assertEqual(200, result.status_code)
            self.assertEqual(6, len(data))

            self.assertEqual(1, data[0]['id'])
            self.assertEqual('username1', data[0]['username'])
            self.assertTrue(data[0]['authenticated'])
            self.assertFalse(data[0]['token'])
            self.assertTrue(data[0]['password'])
            self.assertEqual('username1@foo.com', data[0]['email'])

            self.assertEqual(2, data[1]['id'])
            self.assertEqual('username2', data[1]['username'])
            self.assertFalse(data[1]['authenticated'])
            self.assertFalse(data[1]['token'])
            self.assertTrue(data[1]['password'])
            self.assertEqual('username2@foo.com', data[1]['email'])

    def test_suggest_endpoint(self):
        with self.app:
            login = self.app.post('/api/v1/login', data={'email': 'username@foo.com',
                                  'password': '12345678'})
            result = self.app.get('/api/v1/product_areas')
            data = json.loads(result.data)

            self.assertEqual(200, login.status_code)
            self.assertEqual(404, result.status_code)
            self.assertIn('did you mean /api/v1/productAreas', data['message'])

    def test_get_product_areas(self):
        with self.app:
            login = self.app.post('/api/v1/login', data={'email': 'username@foo.com',
                                  'password': '12345678'})
            result = self.app.get('/api/v1/productAreas')
            data = json.loads(result.data)

            self.assertEqual(200, login.status_code)
            self.assertEqual(200, result.status_code)
            self.assertEqual(4, len(data))

            self.assertEqual(1, data[0]['id'])
            self.assertEqual('Policies', data[0]['name'])

            self.assertEqual(2, data[1]['id'])
            self.assertEqual('Claims', data[1]['name'])

            self.assertEqual(3, data[2]['id'])
            self.assertEqual('Billing', data[2]['name'])

            self.assertEqual(4, data[3]['id'])
            self.assertEqual('Reports', data[3]['name'])

    def test_get_feature_requests(self):
        with self.app:
            login = self.app.post('/api/v1/login', data={'email': 'username@foo.com',
                                  'password': '12345678'})
            result = self.app.get('/api/v1/featureRequests')

            self.assertEqual(200, login.status_code)
            self.assertEqual(200, result.status_code)
            data = json.loads(result.data)
            print data


if __name__ == '__main__':
    unittest.main()
