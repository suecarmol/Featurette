import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..')) # noqa
from app.models import User
from app import app
from app.db import session
from app.db import create_db_tables


class FeatureRequestUnitTest(unittest.TestCase):

    def setUp(self):
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def test_restricted_feature_request_endpoints_without_auth(self):
        with self.app:
            response_features = self.app.get('/api/v1/featureRequests')
            response_add_features = self.app.get('/api/v1/featureRequests')
            self.assertEqual(401, response_features.status_code)
            self.assertEqual(401, response_add_features.status_code)

    def test_restricted_feature_request_endpoints_with_auth(self):
        with self.app:
            user = session.query(User).get(1)
            response = self.app.post('/api/v1/login', data={
                                     'email': user.email,
                                     'password': user.password})
            self.assertTrue(user.authenticated)
            self.assertEqual(200, response.status_code)
            response_features = self.app.get('/api/v1/featureRequests')
            # response_add_features = self.app.get('/addFeature')
            # response_delete_features = self.app.get('/deleteFeature')
            self.assertEqual(200, response_features.status_code)
            # self.assert200(response_add_features)
            # self.assert200(response_delete_features)

if __name__ == '__main__':
    unittest.main()
