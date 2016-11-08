import sys
import os
from flask import Flask
import unittest
from flask_testing import TestCase
from flask_login import current_user
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app.models import User, FeatureRequest
from app import app, db, bcrypt


class FeatureRequestUnitTest(TestCase):

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
        responseFeatures = self.client.get('/')
        responseAddFeatures = self.client.get('/addFeature')
        responseEditFeatures = self.client.get('/editFeature')
        responseDeleteFeatures = self.client.get('/deleteFeature')
        self.assert401(responseFeatures)
        self.assert401(responseAddFeatures)
        self.assert401(responseEditFeatures)
        self.assert401(responseDeleteFeatures)

    def test_restricted_user_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        response = self.client.post('/login', {'email': user.email, 'password':
                                               user.password})
        self.assertTrue(current_user.is_authenticated())
        responseFeatures = self.client.get('/')
        responseAddFeatures = self.client.get('/addFeature')
        responseEditFeatures = self.client.get('/editFeature')
        responseDeleteFeatures = self.client.get('/deleteFeature')
        self.assert200(responseFeatures)
        self.assert200(responseAddFeatures)
        self.assert200(responseEditFeatures)
        self.assert200(responseDeleteFeatures)

if __name__ == '__main__':
    unittest.main()
