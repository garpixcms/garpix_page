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
        self.test_user = baker.make(get_user_model())

    def user_login(self):
        self.client.force_login(self.test_user)
        self.client.force_authenticate(self.test_user)

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
                response = self.client.get(f'/{settings.API_URL}/page/{page.slug}')
                if getattr(page, 'login_required', False):
                    self.assertEqual(response.status_code, 401)
                    self.user_login()
                    response = self.client.get(f'/{settings.API_URL}/page/{page.slug}')
                if not page.has_permission_required(response.wsgi_request):
                    self.user_login()
                    response = self.client.get(f'/{settings.API_URL}/page/{page.slug}')
                    self.assertEqual(response.status_code, 403)
                else:
                    self.assertEqual(response.status_code, 200)
                self.client.logout()
