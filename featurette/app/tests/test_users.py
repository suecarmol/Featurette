import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from flask import Flask
import unittest
from app import app, db
from app.models import User
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy

class UserUnitTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://featurette:br1teCor3@localhost/featurette'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_restricted_user_endpoints_without_auth(self):
        responseUsers = self.client.get('/users')
        responseAddUsers = self.client.get('/addUser')
        responseEditUsers = self.client.get('/editUser')
        responseDeleteUsers = self.client.get('/deleteUser')
        self.assert401(responseUsers)
        self.assert401(responseAddUsers)
        self.assert401(responseEditUsers)
        self.assert401(responseDeleteUsers)

    def test_restricted_user_endpoints_with_auth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        response = self.client.post('/login', { 'email': user.email, 'password': user.password})
        responseUsers = self.client.get('/users')
        responseAddUsers = self.client.get('/addUser')
        responseEditUsers = self.client.get('/editUser')
        responseDeleteUsers = self.client.get('/deleteUser')
        self.assertTrue(current_user.is_authenticated())
        self.assert200(responseUsers)
        self.assert200(responseAddUsers)
        self.assert200(responseEditUsers)
        self.assert200(responseDeleteUsers)

    def test_unauth(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        auth = user.is_authenticated()
        self.assertFalse(auth)

    def test_login(self):
        user = User('username', 'username@foo.com', bcrypt.generate_password_hash('12345678'))
        response = self.client.post('/login', { 'email': user.email, 'password': user.password})
        self.assertEquals(current_user.username, 'username')
        self.assertTrue(current_user.is_authenticated())

    def test_logout(self):
        response = self.client.get('/logout')
        self.assertFalse(current_user.authenticated)


if __name__ == '__main__':
    unittest.main()
