from django.conf import settings
from rest_framework.test import APITestCase

from garpix_page.utils.get_languages import get_languages


class GetLanguagesTest(APITestCase):
    def setUp(self):
        settings.LANGUAGES = (
            ('en', 'English'),
            ('de', 'German'),
            ('ru', 'Russian'),
            ('zh-hans', 'Chinese'),
        )

    def test_get_languages(self) -> None:
        langs = get_languages()
        self.assertEqual(langs, [x[0] for x in settings.LANGUAGES])
