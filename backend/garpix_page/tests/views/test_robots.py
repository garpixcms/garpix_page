from unittest.mock import MagicMock

from django.core.cache import cache
from django.contrib.sites.models import Site
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from model_bakery import baker

from garpix_page.models import GarpixPageSiteConfiguration

class RobotsTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        cache.clear()
        GarpixPageSiteConfiguration.objects.all().delete()

        site = Site.objects.get_current()
        self.config = baker.make(
            GarpixPageSiteConfiguration,
            site=site,
            robots_txt="test",
        )

    def test_robots_txt(self) -> None:
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b"test")

    def test_robots_txt_blank(self) -> None:
        GarpixPageSiteConfiguration.get_solo = MagicMock(side_effect=Exception("test"))
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b"")
