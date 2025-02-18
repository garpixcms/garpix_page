from unittest.mock import MagicMock

from django.utils import translation
from django.conf import settings
from rest_framework.test import APITestCase

from garpix_page.utils.get_current_language_code_url_prefix import (
    get_current_language_code_url_prefix,
)


class GetCurrentLanguageUrlTest(APITestCase):
    def test_get_current_language_url(self) -> None:
        translation.get_language = MagicMock(return_value="eu")
        current_language = translation.get_language()
        settings.USE_DEFAULT_LANGUAGE_PREFIX = True
        settings.LANGUAGE_CODE = "eu"
        current_url_prefix = get_current_language_code_url_prefix()
        self.assertEqual(current_url_prefix, "/" + current_language)

    def test_get_current_laguage_url_void(self) -> None:
        translation.get_language = MagicMock(return_value="eu")
        current_language = translation.get_language()
        settings.USE_DEFAULT_LANGUAGE_PREFIX = False
        settings.LANGUAGE_CODE = current_language
        current_url_prefix = get_current_language_code_url_prefix()
        self.assertEqual(current_url_prefix, "")
        
        settings.USE_DEFAULT_LANGUAGE_PREFIX = True
        translation.get_language = MagicMock(return_value=None)
        current_url_prefix = get_current_language_code_url_prefix()
        self.assertEqual(current_url_prefix, "")
