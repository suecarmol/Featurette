import sys
import os
import unittest

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
        with self.app:
            response_product_areas = self.app.get('/api/v1/productAreas')
            response_add_product_areas = self.app.post('/api/v1/productAreas',
                                                       data={'name': 'Test1'})
            response_delete_product_areas = self.app.delete('/api/v1/productArea/5')
            self.assertEqual(401, response_product_areas.status_code)
            self.assertEqual(401, response_add_product_areas.status_code)
            self.assertEqual(401, response_delete_product_areas.status_code)

    def test_restricted_product_area_endpoints_with_auth(self):
        with self.app:
            user = session.query(User).get(1)
            response = self.app.post('/api/v1/login', data={
                                     'email': user.email,
                                     'password': user.password})
            self.assertEqual(200, response.status_code)
            self.assertTrue(user.authenticated)
            response_product_areas = self.app.get('/api/v1/productAreas')
            response_add_product_areas = self.app.post('/api/v1/productAreas',
                                                       data={'name': 'Test1'})
            response_delete_product_areas = self.app.delete('/api/v1/productArea/5')
            self.assertEqual(200, response_product_areas.status_code)
            self.assertEqual(200, response_add_product_areas.status_code)
            self.assertEqual(200, response_delete_product_areas.status_code)

    def test_add_product_area(self):
        with self.app:
            product_area = 'Product Area 1'
            response = self.app.post('/api/v1/productAreas',
                                     {'name': product_area})
            self.assertEqual(401, response.status_code)

if __name__ == '__main__':
    unittest.main()
