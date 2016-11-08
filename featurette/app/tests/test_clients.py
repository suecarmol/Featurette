import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from flask import Flask
from app import app, db
import unittest
from app.models import User, Client
from flask_testing import TestCase

class ClientUnitTest(TestCase):

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
        responseClients = self.client.get('/clients')
        responseAddClients = self.client.get('/addClient')
        responseEditClients = self.client.get('/editClient')
        responseDeleteClients = self.client.get('/deleteClient')
        self.assert401(responseClients)
        self.assert401(responseAddClients)
        self.assert401(responseEditClients)
        self.assert401(responseDeleteClients)

    def test_restricted_user_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        response = self.client.post('/login', { 'email': user.email, 'password': user.password})
        responseClients = self.client.get('/clients')
        responseAddClients = self.client.get('/addClient')
        responseEditClients = self.client.get('/editClient')
        responseDeleteClients = self.client.get('/deleteClient')
        self.assertTrue(current_user.is_authenticated())
        self.assert200(responseClients)
        self.assert200(responseAddClients)
        self.assert200(responseEditUsers)
        self.assert200(responseDeleteClients)

if __name__ == '__main__':
    unittest.main()
