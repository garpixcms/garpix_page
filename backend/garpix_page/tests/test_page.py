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

    def test_page(self):
        for page in self.pages:
            response = self.client.get(f'/{page.slug}')
            if page.login_required():
                self.assertEqual(response.status_code, 302)
                self.client.force_authenticate(user=self.test_user)
                response = self.client.get(f'/{page.slug}')
            if not page.user_has_permission_required(self.test_user):
                self.assertEqual(response.status_code, 302)
            else:
                self.assertEqual(response.status_code, 200)
            self.client.logout()

    def test_page_api(self):
        if hasattr(settings, 'GARPIX_PAGE_API_URL'):
            for page in self.pages:
                response = self.client.get(f'/{settings.GARPIX_PAGE_API_URL}{page.slug}')
                if page.login_required():
                    self.assertEqual(response.status_code, 401)
                    self.client.force_authenticate(user=self.test_user)
                    response = self.client.get(f'/{settings.GARPIX_PAGE_API_URL}{page.slug}')
                if not page.user_has_permission_required(self.test_user):
                    self.client.force_authenticate(user=self.test_user)
                    response = self.client.get(f'/{settings.GARPIX_PAGE_API_URL}{page.slug}')
                    self.assertEqual(response.status_code, 403)
                else:
                    self.assertEqual(response.status_code, 200)
                self.client.logout()

    # def test_page_admin(self):
    #     self.client.force_authenticate(user=self.test_user)
    #     response = self.client.get('/admin/garpix_page/basepage/')
    #     print(response.request)
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.client.get('/admin/garpix_page/basepage/add/')
    #     self.assertEqual(response.status_code, 200)
    #
    #     for page in self.pages:
    #         page_ct = ContentType.objects.get_for_model(page)
    #         response = self.client.get(f'/admin/garpix_page/basepage/add/?ct_id={page_ct}')
    #         self.assertEqual(response.status_code, 200)
