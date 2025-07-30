from django.contrib.sites.models import Site
from rest_framework.test import APITestCase

from garpix_page.utils.all_sites import get_all_sites

class GetAllSitesTest(APITestCase):
    def setUp(self) -> None:
        Site.objects.all().delete()
        Site.objects.bulk_create(
            [Site(domain=f"domain{i}", name=f"name{i}") for i in range(5)]
        )
        self.sites = Site.objects.all()

    def test_get_all_sites(self) -> None:
        sites = get_all_sites()
        self.assertFalse(bool(set(sites).difference(self.sites)))
