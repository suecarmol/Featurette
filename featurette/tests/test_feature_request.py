import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..')) # noqa
from app import app
from config import config
from app.db import create_db_tables
from app.db import delete_db_tables


class FeatureRequestUnitTest(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config['test'])
        app.login_manager.init_app(app)
        app.test_mode = True
        self.app = app.test_client()
        create_db_tables

    def tearDown(self):
        app.test_mode = False
        delete_db_tables

    def test_get_all_feature_requests(self):
        with self.app:
            response_all_feat_req = self.app.get('/api/v1/featureRequests')
            self.assertEqual(200, response_all_feat_req.status_code)

    def test_get_one_feature_request(self):
        with self.app:
            response_one_feat_req = self.app.get('/api/v1/featureRequest/1')
            self.assertEqual(200, response_one_feat_req.status_code)

    def test_add_feature_request(self):
        with self.app:
            response_add_feat_req = self.app.post('/api/v1/featureRequests',
                                                  data={'title': 'Great Title',
                                                        'description': 'A description',
                                                        'client_id': 1,
                                                        'client_priority': 2,
                                                        'product_area_id': 1,
                                                        'target_date': '2017-01-09',
                                                        'ticket_url': 'www.wired.com',
                                                        })
            self.assertEqual(201, response_add_feat_req.status_code)

    def test_edit_feature_request(self):
        with self.app:
            resp_edit_feat_req = self.app.put('/api/v1/featureRequest/1',
                                              data={'title': 'Great Title',
                                                    'description': 'A description',
                                                    'client_id': 1,
                                                    'client_priority': 99,
                                                    'product_area_id': 1,
                                                    'target_date': '2017-01-09',
                                                    'ticket_url': 'www.apple.com'
                                                    })
            self.assertEqual(201, resp_edit_feat_req.status_code)

    def test_delete_feature_request(self):
        with self.app:
            response_del_feat_req = self.app.delete('/api/v1/featureRequest/2')
            self.assertEqual(200, response_del_feat_req.status_code)

if __name__ == '__main__':
    unittest.main()
