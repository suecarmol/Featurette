import sys
import os
import unittest
import requests

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..')) # noqa
from app import app, bcrypt
from app.models import User
from app.db import create_db_tables
from app.db import session


class ProductAreaUnitTest(unittest.TestCase):

    def setUp(self):
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def test_restricted_product_area_endpoints_without_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash
                    ('12345678'))
        session.add(user)
        session.commit()
        assert user in session
        response_login = requests.post('http://127.0.0.1:5000/api/v1/login', data={
                                            'email': user.email,
                                            'password': user.password})
        self.assertEqual(200, response_login.status_code)
        self.assertTrue(user.authenticated)
        response_logout = requests.post('http://127.0.0.1:5000/api/v1/logout')
        self.assertEqual(200, response_logout.status_code)
        response_product_areas = requests.get('http://127.0.0.1:5000/api/v1/productAreas')
        response_add_product_areas = requests.post('http://127.0.0.1:5000/api/v1/productAreas',
                                                   data={'name': 'Test1'})
        response_delete_product_areas = requests.delete('http://127.0.0.1:5000/api/v1/productArea/5')
        self.assertFalse(user.authenticated)
        self.assertEqual(401, response_product_areas.status_code)
        self.assertEqual(401, response_add_product_areas.status_code)
        self.assertEqual(401, response_delete_product_areas.status_code)

    def test_restricted_product_area_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash
                    ('12345678'))
        session.add(user)
        session.commit()
        assert user in session
        response = requests.post('http://127.0.0.1:5000/api/v1/login', data={
                                 'email': user.email,
                                 'password': user.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue(user.authenticated)
        response_product_areas = requests.get('http://127.0.0.1:5000/api/v1/productAreas')
        response_add_product_areas = requests.post('http://127.0.0.1:5000/api/v1/productAreas',
                                                   data={'name': 'Test1'})
        response_delete_product_areas = requests.delete('http://127.0.0.1:5000/api/v1/productArea/5')
        self.assertEqual(200, response_product_areas.status_code)
        self.assertEqual(200, response_add_product_areas.status_code)
        self.assertEqual(200, response_delete_product_areas.status_code)

    def test_add_product_area(self):
        product_area = 'Product Area 1'
        response = requests.post('http://127.0.0.1:5000/api/v1/productAreas',
                                 {'name': product_area})
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()
