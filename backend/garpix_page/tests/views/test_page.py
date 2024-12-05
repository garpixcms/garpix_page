from unittest.mock import MagicMock

from model_bakery import baker
from django.conf import settings
from django.contrib.sites.models import Site
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from garpix_page.views.page import PageView
from garpix_page.models.base_page import BasePage
from app.models.page import Page


class PageViewGetTest(APITestCase):
    def setUp(self) -> None:
        BasePage.objects.all().delete()
        self.client = APIClient()
        self.page = baker.make(Page, url="/index/page", sites=Site.objects.all())
    
    def test_page_view_redirect_by_slash(self) -> None:
        response = self.client.get("/index/page/?index=1&page=2")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/index/page?index=1&page=2")
    
    def test_page_view_render_not_found(self) -> None:
        PageView.get_object = MagicMock(return_value=None)
        response = self.client.get("/index/page")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_page_view_redirect_unauthenticate(self) -> None:
        page = self.page
        setattr(page, "login_required", True)
        PageView.get_object = MagicMock(return_value=page)
        response = self.client.get("/index/page")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, settings.LOGIN_URL)
    
    def test_page_view_redirect_by_context(self) -> None:
        PageView.get_object = MagicMock(return_value=self.page)
        self.page.get_context = MagicMock(return_value={"redirect": "/index/redirect"})
        response = self.client.get("/index/page")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/index/redirect")
    
    def test_page_view_render_to_response(self) -> None:
        PageView.get_object = MagicMock(return_value=self.page)
        response = self.client.get("/index/page")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PageViewPostTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.page = baker.make(Page, url="/index/page", sites=Site.objects.all())

    def test_page_view_redirect_unauthentication(self) -> None:
        page = self.page
        setattr(page, "login_required", True)
        PageView.get_object = MagicMock(return_value=page)
        response = self.client.post("/index/page")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, settings.LOGIN_URL)

    def test_page_view_redirect_by_context(self) -> None:
        PageView.get_object = MagicMock(return_value=self.page)
        self.page.get_context = MagicMock(return_value={"redirect": "/index/redirect"})
        response = self.client.post("/index/page")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/index/redirect")

    def test_page_view_render_to_response(self) -> None:
        PageView.get_object = MagicMock(return_value=self.page)
        response = self.client.get("/index/page")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
