from rest_framework import status
from rest_framework.test import APITestCase

from app.mixins import TestLoginMixin

URL = 'http://127.0.0.1:8000/api/v1/cargo/'


class ViewSetTestCargo(APITestCase, TestLoginMixin):
    def setUp(self):
        self.user_login()
        self.url = URL + 'cargo/'
        self.cargo = {
            "title": "testic",
            "length": 211,
            "width": 2147,
            "height": 2143,
            "mass": 214,
            "fragile": True,
            "is_rotatable": True,
            "article": "test",
            "indentation_l": 0,
            "indentation_w": 0,
            "overhang_angle": 50,
            "color": "#001110"
        }

    def test_create(self):
        response = self.client_api.post(self.url, self.cargo, format='json')
        if response.status_code != 201:
            print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get(self):
        response = self.client_api.get(self.url)
        if response.status_code != 200:
            print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
