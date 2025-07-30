import json
from typing import List, Dict
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response
from model_bakery import baker

from garpix_page.cache import cache_service
from garpix_page.utils.get_languages import get_languages
from app.models.page import Page


class PageApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        sites = Site.objects.all()
        self._delete_all_pages()

        self.page = baker.make(Page, slug="index/page", sites=sites)
        self.test_user = baker.make(get_user_model())
        self.languages_list = get_languages()
    
    def test_page_api_unauthenticate(self) -> None:
        page = self.page
        setattr(page, "login_required", True)
        with patch("garpix_page.views.page_api.PageApiView.get_object", return_value=page):
            responses = self._generate_responses_list(page)
            self._check_response_status(responses, 401)
            self._check_response_data(
                responses,
                {
                    "page_model": "Page401",
                    "init_state": {
                        "object": None,
                        "global": {},
                    }
                },
            )

    def test_page_api_permission_denied(self) -> None:
        with patch("app.models.page.Page.has_permission_required", return_value=False):
            responses = self._generate_responses_list(self.page)
            self._check_response_status(responses, 403)
            self._check_response_data(
                responses,
                {
                    "page_model": "Page403",
                    "init_state": {
                        "object": None,
                        "global": {},
                    }
                },
            )
    
    def test_page_api_success(self) -> None:
        with patch("app.models.page.Page.has_permission_required", return_value=True):
            responses = self._generate_responses_list(self.page)
            self._check_response_status(responses, 200)


    def _user_login(self) -> None:
        self.client.force_login(self.test_user)
        self.client.force_authenticate(self.test_user)

    def _generate_responses_list(self, page) -> List[Response]:
        responses = [
            (self.client.get(f'/{settings.API_URL}/page{page.url}'), page),
            (self.client.get(f'/{settings.API_URL}/page{page.url}/'), page)
        ]
        for language in self.languages_list:
            responses.append((self.client.get(f'/{settings.API_URL}/page/{language}{page.url}'), page))
            responses.append((self.client.get(f'/{settings.API_URL}/page/{language}{page.url}/'), page))
            cache_service.clear_all()
        return responses

    def _check_response_status(self, responses: List[Response], status_code: int=None, equal: bool=True) -> None:
        if not status_code:
            for response in responses:
                self.assertNotRegex(str(response[0].status_code), r'^5\d{2}$',
                                    f'Error in page api of {response[1]} ({response[1].model_name()})')
        else:
            for response in responses:
                if equal:
                    self.assertEqual(response[0].status_code, status_code,
                                     f'Error in page api of {response[1]} ({response[1].model_name()})')
                else:
                    self.assertNotEqual(response[0].status_code, status_code,
                                        f'Error in page api of {response[1]} ({response[1].model_name()})')
                    
    def _check_response_data(self, responses: List[Response], data: Dict[str, str]) -> None:
        for response in responses:
            self.assertEqual(json.loads(response[0].content), data)
                    
    def _delete_all_pages(self) -> None:
        Page.objects.all().delete()
