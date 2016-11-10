import os
import sys
import unittest

from flask_testing import TestCase
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
from app import app, bcrypt, db
from app.models import User


class UserUnitTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_restricted_user_endpoints_without_auth(self):
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = self.client.post('/login', {'email': user.email,
                                    'password': user.password})
        self.assert200(response)
        logout = self.client.get('/logout')
        response_users = self.client.get('/users')
        response_add_users = self.client.get('/addUser')
        response_edit_users = self.client.get('/editUser')
        response_delete_users = self.client.get('/deleteUser')
        self.assert200(logout)
        self.assert401(response_users)
        self.assert401(response_add_users)
        self.assert401(response_edit_users)
        self.assert401(response_delete_users)

    def test_restricted_user_endpoints_with_auth(self):
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = self.client.post('/login', {'email': user.email,
                                    'password': user.password})
        self.assertTrue(user.authenticated)
        response_users = self.client.get('/users')
        response_add_users = self.client.get('/addUser')
        response_edit_users = self.client.get('/editUser')
        response_delete_users = self.client.get('/deleteUser')
        self.assert200(response)
        self.assert200(response_users)
        self.assert200(response_add_users)
        self.assert200(response_edit_users)
        self.assert200(response_delete_users)

    def test_unauth(self):
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        self.assertFalse(user.authenticated)

    def test_login(self):
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = self.client.post('/login', {'email': user.email,
                                               'password': user.password})
        self.assert200(response)
        self.assertEquals(user.username, 'username')
        self.assertTrue(user.authenticated)

    def test_logout(self):
        # logging in
        user = User('username', 'username@foo.com',
                    bcrypt.generate_password_hash('12345678'))
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response_login = self.client.post('/login', {'email': user.email,
                                                     'password': user.password})
        self.assertRedirects(response_login, '/')
        self.assertTrue(user.authenticated)
        # logging out
        response_logout = self.client.get('/logout')
        # assert that logout was made
        self.assert200(response_logout)
        self.assertFalse(user.authenticated)


if __name__ == '__main__':
    unittest.main()
