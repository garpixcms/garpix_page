from typing import List

from django.contrib.sites.models import Site
from rest_framework.test import APITestCase

from garpix_page.utils.check_sites import check_sites

class CheckSitesTest(APITestCase):
    class parent:
        def __init__(self, sites: List[Site] = None):
            self.sites = sites

    def setUp(self) -> None:
        Site.objects.all().delete()
        Site.objects.bulk_create(
            [Site(domain=f"domain{i}", name=f"name{i}") for i in range(5)]
        )
        self.sites = Site.objects.all()

    def test_check_sites_intersect_all(self) -> None:
        parent = self.parent(sites=self.sites)
        cleaned_data = {
            "sites": self.sites,
            "parent": parent,
        }
        self.assertTrue(check_sites(cleaned_data))

    def test_check_sites_intersect_one(self) -> None:
        parent = self.parent(sites=self.sites[:1])
        cleaned_data = {
            "sites": self.sites,
            "parent": parent,
        }
        self.assertTrue(check_sites(cleaned_data))

    def test_check_sites_none(self) -> None:
        parent = self.parent(sites=self.sites)
        cleaned_data = {
            "sites": None,
            "parent": parent,
        }
        self.assertTrue(check_sites(cleaned_data))

    def test_check_sites_none_parent(self) -> None:
        cleaned_data = {
            "sites": self.sites,
            "parent": None,
        }
        self.assertTrue(check_sites(cleaned_data))

    def test_check_sites_invalid(self) -> None:
        parent = self.parent(sites=self.sites[3:])
        cleaned_data = {
            "sites": self.sites[:3],
            "parent": parent,
        }
        self.assertFalse(check_sites(cleaned_data))
