from model_bakery import baker
from django.contrib.sites.models import Site
from rest_framework.test import APITestCase

from garpix_page.models.base_page import BasePage
from garpix_page.tasks.update_child_urls import clear_child_cache


class UpdateChildUrlsTaskTest(APITestCase):
    def setUp(self) -> None:
        BasePage.objects.all().delete()

        sites = Site.objects.all()
        self.base_page = baker.make(BasePage, slug="index", sites=sites)
        for i in range(2):
            child_page = baker.make(BasePage, slug=f"child{i}", parent=self.base_page, sites=sites)
            for j in range(2):
                baker.make(BasePage, slug=f"garndchild{j}", parent=child_page, sites=sites)

    def test_start_position(self) -> None:
        pages = self.base_page.get_descendants(include_self=True)
        for page in pages:
            self.assertEqual(page.url, "/")
    
    def test_update_child_urls(self) -> None:
        clear_child_cache(self.base_page.id)

        self.assertEqual(self.base_page.url, "/index")
        for child in self.base_page.get_children():
            self.assertEqual(child.url, f"/{self.base_page.slug}/{child.slug}")
            for grandchild in child.get_children():
                self.assertEqual(grandchild.url, f"/{self.base_page.slug}/{child.slug}/{grandchild.slug}")
