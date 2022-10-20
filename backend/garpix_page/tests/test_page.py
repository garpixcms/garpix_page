from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from rest_framework.test import APIClient, APITestCase
from model_bakery import baker

from ..utils.get_garpix_page_models import get_garpix_page_models
from ..cache import cache_service
from ..utils.get_languages import get_languages


class BasePageApiTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.update_baker_default_mapping()
        super().setUpClass()

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
        self.languages_list = get_languages()

    def test_page(self):
        for page in self.pages:
            response = self.client.get(f'/{page.slug}')
            if getattr(page, 'login_required', False):
                self.assertEqual(response.status_code, 302, f'Error in page {page} ({page.model_name()})')
                self.user_login()
                response = self.client.get(f'/{page.slug}')
            if not page.has_permission_required(response.wsgi_request):
                self.assertEqual(response.status_code, 302, f'Error in page {page} ({page.model_name()})')
            else:
                self.assertNotRegex(str(response.status_code), r'^5\d{2}$',
                                    f'Error in page {page} ({page.model_name()})')
                self.assertNotEqual(response.status_code, 404,
                                    f'Error in page {page} ({page.model_name()})')
            self.client.logout()

    def test_page_api(self):
        if hasattr(settings, 'API_URL'):
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
            (self.client.get(f'/{settings.API_URL}/page/{page.slug}'), page),
            (self.client.get(f'/{settings.API_URL}/page/{page.slug}/'), page)
        ]
        for language in self.languages_list:
            responses.append((self.client.get(f'/{settings.API_URL}/page/{language}/{page.slug}'), page))
            responses.append((self.client.get(f'/{settings.API_URL}/page/{language}/{page.slug}/'), page))
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

    @staticmethod
    def update_baker_default_mapping():

        def gen_phone_number() -> str:
            import random
            import string
            return f"+{''.join(random.SystemRandom().choice(string.digits) for _ in range(15))}"

        from model_bakery import random_gen
        from model_bakery.generators import default_mapping

        try:
            from ckeditor.fields import RichTextField
        except ImportError:
            RichTextField = None

        try:
            from ckeditor_uploader.fields import RichTextUploadingField
        except ImportError:
            RichTextUploadingField = None

        try:
            from phonenumber_field.modelfields import PhoneNumberField
        except ImportError:
            PhoneNumberField = None

        default_mapping.update({
            RichTextField: random_gen.gen_text,
            RichTextUploadingField: random_gen.gen_text,
            PhoneNumberField: gen_phone_number
        })
