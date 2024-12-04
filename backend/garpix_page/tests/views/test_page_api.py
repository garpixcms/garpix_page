from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from rest_framework.test import APIClient, APITestCase
from model_bakery import baker

from garpix_page.models import BasePage
from garpix_page.utils.get_garpix_page_models import get_garpix_page_models
from garpix_page.cache import cache_service
from garpix_page.utils.get_languages import get_languages


class PageApiTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        page_models = get_garpix_page_models()
        sites = Site.objects.all()

        self.pages = []
        for index, page_model in enumerate(page_models):
            page = baker.make(page_model, slug=f'slug{index}', sites=sites)
            self.pages.append(page)

        if len(page_models) > 0:
            page = baker.make(page_models[0], slug='', sites=sites)
            self.pages.append(page)

        self.test_user = baker.make(get_user_model())
        self.languages_list = get_languages()

    # def test_page(self):
    #     for page in self.pages:
    #         response = self.client.get(page.url)
    #         if getattr(page, 'login_required', False):
    #             self.assertEqual(response.status_code, 302, f'Error in page {page} ({page.model_name()})')
    #             self.user_login()
    #             response = self.client.get(page.url)
    #         if not page.has_permission_required(response.wsgi_request):
    #             self.assertEqual(response.status_code, 302, f'Error in page {page} ({page.model_name()})')
    #         else:
    #             self.assertNotRegex(str(response.status_code), r'^5\d{2}$',
    #                                 f'Error in page {page} ({page.model_name()})')
    #             self.assertNotEqual(response.status_code, 404,
    #                                 f'Error in page {page} ({page.model_name()})')
    #         self.client.logout()

    def test_page_api(self):
        if not hasattr(settings, 'API_URL'):
            return
        
        for page in self.pages:
            responses = self.generate_responses_list(page)

            if getattr(page, 'login_required', False):
                self.check_response_status(responses, 401)
                self.user_login()
                responses = self.generate_responses_list(page)
                
            if not page.has_permission_required(responses[0][0].wsgi_request):
                self.user_login()
                responses = self.generate_responses_list(page)
                self.check_response_status(responses, 403)
            else:
                self.check_response_status(responses)
                self.check_response_status(responses, 404, equal=False)
            self.client.logout()

    def user_login(self):
        self.client.force_login(self.test_user)
        self.client.force_authenticate(self.test_user)

    def generate_responses_list(self, page):
        responses = [
            (self.client.get(f'/{settings.API_URL}/page{page.url}'), page),
            (self.client.get(f'/{settings.API_URL}/page{page.url}/'), page)
        ]
        for language in self.languages_list:
            responses.append((self.client.get(f'/{settings.API_URL}/page/{language}{page.url}'), page))
            responses.append((self.client.get(f'/{settings.API_URL}/page/{language}{page.url}/'), page))
            cache_service.clear_all()
        return responses

    def check_response_status(self, responses, status_code=None, equal=True):
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
