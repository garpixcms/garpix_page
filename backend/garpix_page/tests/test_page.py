from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from rest_framework.test import APIClient, APITestCase
from model_bakery import baker

from ..utils.get_garpix_page_models import get_garpix_page_models


class BasePageApiTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        page_models = get_garpix_page_models()
        sites = Site.objects.all()

        self.pages = []
        i = 0
        for page_model in page_models:
            page = baker.make(page_model, slug=f'slug{i}', sites=sites)
            self.pages.append(page)
            i += 1
        if len(page_models) > 0:
            page = baker.make(page_models[0], slug='', sites=sites)
            self.pages.append(page)
        self.test_user = baker.make(get_user_model())
        self.languages_list = [x[0] for x in settings.LANGUAGES]

    def user_login(self):
        self.client.force_login(self.test_user)
        self.client.force_authenticate(self.test_user)

    def generate_responses_list(self, page):
        responses = [
            self.client.get(f'/{settings.API_URL}/page/{page.slug}'),
            self.client.get(f'/{settings.API_URL}/page/{page.slug}/')
        ]
        for language in self.languages_list:
            responses.append(self.client.get(f'/{settings.API_URL}/page/{language}/{page.slug}'))
            responses.append(self.client.get(f'/{settings.API_URL}/page/{language}/{page.slug}/'))
        return responses

    def check_response_status(self, responses, status_code):
        for response in responses:
            self.assertEqual(response.status_code, status_code)

    def test_page(self):
        for page in self.pages:
            response = self.client.get(f'/{page.slug}')
            if getattr(page, 'login_required', False):
                self.assertEqual(response.status_code, 302)
                self.user_login()
                response = self.client.get(f'/{page.slug}')
            if not page.has_permission_required(response.wsgi_request):
                self.assertEqual(response.status_code, 302)
            else:
                self.assertEqual(response.status_code, 200)
            self.client.logout()

    def test_page_api(self):
        if hasattr(settings, 'API_URL'):
            for page in self.pages:
                responses = self.generate_responses_list(page)
                if getattr(page, 'login_required', False):
                    self.check_response_status(responses, 401)
                    self.user_login()
                    responses = self.generate_responses_list(page)
                if not page.has_permission_required(responses[0].wsgi_request):
                    self.user_login()
                    responses = self.generate_responses_list(page)
                    self.check_response_status(responses, 403)
                else:
                    self.check_response_status(responses, 200)
                self.client.logout()
