import sys
import os
import unittest

from flask_testing import TestCase
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from app import app, db, bcrypt
from app.models import User, ProductArea


class ProductAreaUnitTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_restricted_product_area_endpoints_without_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response_login = self.client.post('/login', {'email': user.email,
                                                     'password': user.password})
        self.assert200(response_login)
        self.assertTrue(user.authenticated)
        response_logout = self.client.get('/logout')
        self.assert200(response_logout)
        response_product_areas = self.client.get('/productArea')
        response_add_product_areas = self.client.get('/addProductArea')
        response_edit_product_areas = self.client.get('/editProductArea')
        response_delete_product_areas = self.client.get('/deleteProductArea')
        self.assertFalse(user.authenticated)
        self.assert401(response_product_areas)
        self.assert401(response_add_product_areas)
        self.assert401(response_edit_product_areas)
        self.assert401(response_delete_product_areas)

    def test_restricted_product_area_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = self.client.post('/login', {'email': user.email, 'password':
                                               user.password})
        self.assert200(response)
        self.assertTrue(user.authenticated)
        response_product_areas = self.client.get('/productArea')
        response_add_product_areas = self.client.get('/addProductArea')
        response_edit_product_areas = self.client.get('/editProductArea')
        response_delete_product_areas = self.client.get('/deleteProductArea')
        self.assert200(response_product_areas)
        self.assert200(response_add_product_areas)
        self.assert200(response_edit_product_areas)
        self.assert200(response_delete_product_areas)

    def test_add_product_area(self):
        product_area = ProductArea('Product Area 1')
        response = self.client.post('/addClient', {'name': product_area.name})
        db.session.add(product_area)
        db.session.commit()
        assert product_area in db.session
        self.assert200(response)
        self.assertRedirects(response, '/productAreas')

if __name__ == '__main__':
    unittest.main()
