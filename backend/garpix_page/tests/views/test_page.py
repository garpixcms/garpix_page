from unittest.mock import patch

from model_bakery import baker
from django.conf import settings
from django.contrib.sites.models import Site
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.models.page import Page


class PageViewGetTest(APITestCase):
    def setUp(self) -> None:
        self._delete_all_pages()
        self.client = APIClient()
        self.page = baker.make(Page, slug="index/page", sites=Site.objects.all())
    
    def test_page_view_redirect_by_slash(self) -> None:
        response = self.client.get("/index/page/?index=1&page=2")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "/index/page?index=1&page=2")
    
    def test_page_view_render_not_found(self) -> None:
        self._delete_all_pages()
        response = self.client.get("/index/page")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_page_view_redirect_unauthenticate(self) -> None:
        page = self.page
        setattr(page, "login_required", True)
        with patch("garpix_page.views.page.PageView.get_object", return_value=page):
            response = self.client.get("/index/page")
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.assertEqual(response.url, settings.LOGIN_URL)
    
    def test_page_view_redirect_by_context(self) -> None:
        with patch("garpix_page.views.page.PageView.get_context_data", return_value={"redirect": "/index/redirect"}):
            response = self.client.get("/index/page")
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.assertEqual(response.url, "/index/redirect")
    
    def test_page_view_render_to_response(self) -> None:
        response = self.client.get("/index/page")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def _delete_all_pages(self) -> None:
        Page.objects.all().delete()

class PageViewPostTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.page = baker.make(Page, slug="index/page", sites=Site.objects.all())

    def test_page_view_redirect_unauthentication(self) -> None:
        page = self.page
        setattr(page, "login_required", True)
        with patch("garpix_page.views.page.PageView.get_object", return_value=page):
            response = self.client.post("/index/page")
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.assertEqual(response.url, settings.LOGIN_URL)

    def test_page_view_redirect_by_context(self) -> None:
        with patch("garpix_page.views.page.PageView.get_context_data", return_value={"redirect": "/index/redirect"}):
            response = self.client.post("/index/page")
            self.assertEqual(response.status_code, status.HTTP_302_FOUND)
            self.assertEqual(response.url, "/index/redirect")

    def test_page_view_render_to_response(self) -> None:
        response = self.client.post("/index/page")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
