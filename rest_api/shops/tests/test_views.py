from django.test import TestCase
from http import HTTPStatus
from shops.models import City, Street, Shop
from shops.config import STREET, CITY, STATE_SHOP, SHOP_OPEN, SHOP_CLOSED
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient


class CityViewTest(TestCase):

    def test_get_city_list(self):
        response = self.client.get('/city')

        self.assertEqual(response.status_code, HTTPStatus.OK)


class StreetViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.city_id = City.objects.create(name='city_test').id

    def test_get_street_list(self):
        response = self.client.get(f'/{self.city_id}/street')

        self.assertEqual(response.status_code, HTTPStatus.OK)


class ShopListCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.city_obj = City.objects.create(name='city_test')
        cls.city_id = cls.city_obj.id
        cls.street_obj = Street.objects.create(name='street_test', city=cls.city_obj)
        cls.street_id = cls.street_obj.id

        cls.username = 'test_username'
        cls.password = 'test_password'
        cls.user_obj = get_user_model().objects.create(username=cls.username, password=cls.password)
        cls.user_id = cls.user_obj.id

        cls.client = APIClient()
        cls.token = cls.client.post('/auth/authorization',
                                    {'username': cls.username,
                                     'password': cls.password}).json()['token']

        from datetime import time
        from random import randint
        for i in range(10):
            opening_hour, opening_min, opening_sec = randint(0, 23), randint(0, 59), randint(0, 59)
            closing_hour, closing_min, closing_sec = randint(0, 23), randint(0, 59), randint(0, 59)
            Shop.objects.create(name=f'shop_{i}',
                                user=cls.user_obj,
                                city=cls.city_obj,
                                street=cls.street_obj,
                                house=i,
                                opening_time=time(opening_hour, opening_min, opening_sec),
                                closing_time=time(closing_hour, closing_min, closing_sec)
                                )

    def test_get_shop_list_without_params(self):
        response = self.client.get('/shop')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_shop_list_with_city(self):
        response = self.client.get('/shop', {CITY: self.city_id})
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_shop_list_with_city_and_street(self):
        response = self.client.get('/shop', {CITY: self.city_id,
                                             STREET: self.street_id})
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_shop_list_with_street_and_without_city(self):
        response = self.client.get('/shop', {STREET: self.street_id})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_shop_list_with_city_and_street_state(self):
        response_open = self.client.get('/shop', {CITY: self.city_id,
                                                  STREET: self.street_id,
                                                  STATE_SHOP: SHOP_OPEN})
        response_closed = self.client.get('/shop', {CITY: self.city_id,
                                                    STREET: self.street_id,
                                                    STATE_SHOP: SHOP_CLOSED})

        self.assertEqual(response_open.status_code, HTTPStatus.OK)
        self.assertEqual(response_closed.status_code, HTTPStatus.OK)

    def test_create_shop_unauthorized(self):
        response = self.client.post('/shop', {'name': 'shop_name',
                                              'user': self.user_id,
                                              'city': self.city_id,
                                              'street': self.street_id,
                                              'house': 42,
                                              'opening_time': (8, 0, 0),
                                              'closing_time': (21, 0, 0)})

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_create_shop_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.token}')

        response = self.client.post('/shop', {'name': 'shop_name',
                                              'user': self.user_id,
                                              'city': self.city_id,
                                              'street': self.street_id,
                                              'house': 42,
                                              'opening_time': '08:00:00',
                                              'closing_time': '21:00:00'})

        self.assertEqual(response.status_code, HTTPStatus.OK)