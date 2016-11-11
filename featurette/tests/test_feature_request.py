import sys
import os
import unittest

from flask_testing import TestCase
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app.models import User, FeatureRequest
from app import app, db, bcrypt


class FeatureRequestUnitTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_restricted_feature_request_endpoints_without_auth(self):
        response_logout = self.client.get('/logout')
        self.assert200(response_logout)
        response_features = self.client.get('/')
        response_add_features = self.client.get('/addFeature')
        self.assert200(response_features)
        self.assert200(response_add_features)

    def test_restricted_feature_request_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash
                    ('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = self.client.post('/login', {'email': user.email, 'password':
                                               user.password})
        self.assertRedirects(response, '/')
        self.assertFalse(user.authenticated)
        # response_features = self.client.get('/')
        # response_add_features = self.client.get('/addFeature')
        # response_delete_features = self.client.get('/deleteFeature')
        # self.assert200(response_features)
        # self.assert200(response_add_features)
        # self.assert200(response_delete_features)

if __name__ == '__main__':
    unittest.main()
