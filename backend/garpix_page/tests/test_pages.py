from rest_framework.test import APIClient, APITestCase

from backend.garpix_page.models import BasePage


class BasePageTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_order(self):
        slugs = BasePage.onjects.all().values_list('slug', flat=True)
        print(slugs)
        for slug in slugs:
            response = self.client.get(f'/api/page/{slug}')
            self.assertNotEqual(response.status_code, 500)
