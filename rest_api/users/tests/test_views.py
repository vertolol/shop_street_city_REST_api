from django.test import TestCase, Client
from http import HTTPStatus


class UserCreateTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username = 'test_username'
        cls.password = 'test_password'

    def test_registration(self):
        when_username_not_exists = self.client.post('/auth/registration',
                                                    {'username': self.username,
                                                     'password': self.password})
        when_username_exists = self.client.post('/auth/registration',
                                                {'username': self.username,
                                                 'password': self.password})

        self.assertEqual(when_username_not_exists.status_code, HTTPStatus.OK)
        self.assertEqual(when_username_exists.status_code, HTTPStatus.BAD_REQUEST)


class UserLoginTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username = 'test_username'
        cls.password = 'test_password'
        cls.client = Client()
        registration_user = cls.client.post('/auth/registration',
                                             {'username': cls.username,
                                              'password': cls.password})

    def test_username_and_password_accepted(self):
        response = self.client.post('/auth/authorization',
                                    {'username': self.username,
                                     'password': self.password})

        self.assertTrue('token' in response.json().keys())

    def test_invalid_username(self):
        invalid_username = 'invalid_username'
        response = self.client.post('/auth/authorization',
                                    {'username': invalid_username,
                                     'password': self.password})

        self.assertTrue('error' in response.json().keys())

    def test_invalid_password(self):
        invalid_password = 'invalid_password'
        response = self.client.post('/auth/authorization',
                                    {'username': self.username,
                                     'password': invalid_password})

        self.assertTrue('error' in response.json().keys())
