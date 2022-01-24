from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient, APITestCase

from ..utils.get_garpix_page_models import get_garpix_page_models


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class BasePageTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        page_models = get_garpix_page_models()
        self.pages = []
        i = 0
        for page_model in page_models:
            page = page_model.objects.create(title=f'title_{i}', slug=f'slug_{i}')
            self.pages.append(page)
            i += 1
        self.site = AdminSite()

    def test_page_api(self):
        for page in self.pages:
            response = self.client.get(f'/{settings.GARPIX_PAGE_API_URL}{page.slug}')
            self.assertNotEqual(response.status_code, 500)

    def test_page_admin(self):
        response = self.client.get('/admin/garpix_page/basepage/')
        self.assertNotEqual(response.status_code, 500)

        response = self.client.get('/admin/garpix_page/basepage/add/')
        self.assertNotEqual(response.status_code, 500)

        for page in self.pages:
            page_ct = ContentType.objects.get_for_model(page)
            response = self.client.get(f'/admin/garpix_page/basepage/add/?ct_id={page_ct}')
            self.assertNotEqual(response.status_code, 500)
