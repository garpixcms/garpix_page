from model_bakery import baker
from django.contrib.sites.models import Site
from rest_framework.test import APITestCase

from garpix_page.models.base_page import BasePage
from garpix_page.utils.set_children_urls import set_children_url


class SetChildrenUrlTest(APITestCase):
    def setUp(self) -> None:
        BasePage.objects.all().delete()
        
        sites = Site.objects.all()
        self.base_page = baker.make(BasePage, slug="index", sites=sites)
        self.children = [
            baker.make(BasePage, slug=f"child{i}", sites=sites)
            for i in range(3)
        ]
    
    def test_set_children_test(self) -> None:
        update_pages = []
        set_children_url(self.base_page, self.children, update_pages)

        self.assertEqual(self.children, update_pages)

        for page in self.children:
            self.assertEqual(page.parent, self.base_page)
            self.assertEqual(page.url, f"{self.base_page.url}/{page.slug}")
