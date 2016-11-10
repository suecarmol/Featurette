import sys
import os
from flask import Flask
import unittest
from flask_testing import TestCase
from flask_login import current_user
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from app import app, db, bcrypt
from app.models import User, Client


class ClientUnitTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@127.0.0.1/featurette'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_restricted_client_endpoints_without_auth(self):
        response_clients = self.client.get('/clients')
        response_add_clients = self.client.get('/addClient')
        response_edit_clients = self.client.get('/editClient')
        response_delete_clients = self.client.get('/deleteClient')
        self.assert401(response_clients)
        self.assert401(response_add_clients)
        self.assert401(response_edit_clients)
        self.assert401(response_delete_clients)

    def test_restricted_client_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit
        assert user in db.session
        response = self.client.post('/login', {'email': user.email, 'password':
                                               user.password})
        self.assert200(response)
        self.assertTrue(user.authenticated)
        response_clients = self.client.get('/clients')
        response_add_clients = self.client.get('/addClient')
        response_edit_clients = self.client.get('/editClient')
        response_delete_clients = self.client.get('/deleteClient')
        self.assert200(response_clients)
        self.assert200(response_add_clients)
        self.assert200(response_edit_clients)
        self.assert200(response_delete_clients)

    def test_add_client(self):
        client = Client('Client 1')
        response = self.client.post('/addClient', {'name': client.name})
        db.session.add(client)
        db.session.commit()
        assert client in db.session
        self.assert200(response)
        self.assertRedirects(response, '/clients')

if __name__ == '__main__':
    unittest.main()
