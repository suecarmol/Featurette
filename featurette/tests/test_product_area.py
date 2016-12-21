import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..')) # noqa
from app import app
from config import config
from app.db import create_db_tables
from app.db import delete_db_tables


class ProductAreaUnitTest(unittest.TestCase):

    def setUp(self):
        # LOGIN_DISABLED flag is turned on
        app.config.from_object(config['test'])
        app.login_manager.init_app(app)
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def tearDown(self):
        app.test_mode = False
        delete_db_tables

    def test_get_product_areas(self):
        with self.app:
            response_all_product_areas = self.app.get('/api/v1/productAreas')
            self.assertEqual(200, response_all_product_areas.status_code)

    def test_get_one_product_area(self):
        with self.app:
            response_product_area = self.app.get('/api/v1/productArea/1')
            self.assertEqual(200, response_product_area.status_code)

    def test_add_product_area(self):
        with self.app:
            response_add_product_area = self.app.post('/api/v1/productAreas',
                                                      data={'product_area_name': 'TestPA'})
            self.assertEqual(201, response_add_product_area.status_code)

    def test_edit_product_area(self):
        with self.app:
            response_edit_product_area = self.app.put('/api/v1/productArea/2',
                                                      data={'product_area_name': 'Edited'})
            self.assertEqual(201, response_edit_product_area.status_code)

    def test_delete_product_area(self):
        with self.app:
            response_del_prod_area = self.app.delete('/api/v1/productArea/3')
            self.assertEqual(204, response_del_prod_area.status_code)

if __name__ == '__main__':
    unittest.main()
