from unittest.mock import MagicMock

from django.http.request import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker

from garpix_page.cache.page import cache_service
from garpix_page.views.clear_cache import clear_cache


class ClearCacheViewTest(APITestCase):
    def setUp(self) -> None:
        self.test_user = baker.make(get_user_model())
        self.test_user_unauthenticated = AnonymousUser()

    def test_clear_cache(self) -> None:
        cache_service.clear_all = MagicMock()
        request = HttpRequest()
        request.method = "GET"
        request._messages = type("message", (object,), {"add": lambda *args: None})
        self.user_change_staff()
        request.user = self.test_user
        response = clear_cache(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse("admin:index"))
        self.assertTrue(cache_service.clear_all.called)

        request.META["HTTP_REFERER"] = "/test/index"
        response = clear_cache(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/test/index")
        self.assertTrue(cache_service.clear_all.called)

    def test_clear_cache_invalid(self) -> None:
        cache_service.clear_all = MagicMock()
        request = HttpRequest()
        request.method = "GET"
        request.user = self.test_user_unauthenticated
        response = clear_cache(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse("admin:index"))
        self.assertFalse(cache_service.clear_all.called)
        
        response = clear_cache(request)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, reverse("admin:index"))
        self.assertFalse(cache_service.clear_all.called)

    def user_change_staff(self) -> None:
        self.test_user.is_staff = True
        self.test_user.save()
