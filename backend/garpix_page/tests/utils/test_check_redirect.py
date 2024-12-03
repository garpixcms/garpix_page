from django.contrib.sites.models import Site
from rest_framework.test import APITestCase

from garpix_page.utils.check_redirect import check_redirect

class CheckRedirectTest(APITestCase):
    class request:
        def __init__(self, path: str):
            self.path = path

    def test_check_redirect(self) -> None:
        request = self.request("/index")
        context = {"redirect": "/main"}
        self.assertEqual(check_redirect(request, context), context["redirect"])
    
    def test_invalid_check_redirect(self) -> None:
        request = self.request("/index")
        context = {"redirect": "/index"}
        self.assertEqual(check_redirect(request, context), None)

        request = self.request("/index")
        context = {}
        self.assertEqual(check_redirect(request, context), None)
