import sys
import os
from flask import Flask
import unittest

from flask_testing import TestCase
from flask_login import current_user
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app import app, db, bcrypt
from app.models import User, ProductArea


class ProductAreaUnitTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_restricted_user_endpoints_without_auth(self):
        responseProductAreas = self.client.get('/productArea')
        responseAddProductAreas = self.client.get('/addProductArea')
        responseEditProductAreas = self.client.get('/editProductArea')
        responseDeleteProductAreas = self.client.get('/deleteProductArea')
        self.assert401(responseProductAreas)
        self.assert401(responseAddProductAreas)
        self.assert401(responseEditProductAreas)
        self.assert401(responseDeleteProductAreas)

    def test_restricted_user_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        response = self.client.post('/login', {'email': user.email, 'password':
                                               user.password})
        self.assertTrue(current_user.is_authenticated())
        responseProductAreas = self.client.get('/productArea')
        responseAddProductAreas = self.client.get('/addProductArea')
        responseEditProductAreas = self.client.get('/editProductArea')
        responseDeleteProductAreas = self.client.get('/deleteProductArea')
        self.assert200(response)
        self.assert200(responseProductAreas)
        self.assert200(responseAddProductAreas)
        self.assert200(responseEditProductAreas)
        self.assert200(responseDeleteProductAreas)

if __name__ == '__main__':
    unittest.main()
