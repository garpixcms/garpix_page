from typing import List
from unittest.mock import patch

from rest_framework.test import APITestCase

from garpix_page.utils.get_exclude_fields import get_exclude_fields


class GetExcludeFieldsTest(APITestCase):
    class model:
        def __init__(self, *fields: List[str]):
            self._meta = type(
                "_meta",
                (object,),
                {
                    "get_fields": lambda: [
                        type("field", (object,), {"name": name})
                        for name in fields
                    ],
                }
            )

    def setUp(self):
        self.models = [
            (
                self.model("field", "field_eu", "field_ru"),
                ["field_eu", "field_ru"],
            ),
            (
                self.model("field1", "field1_eu", "field1_ru",
                           "field2", "field2_eu", "field2_ru"),
                ["field1_eu", "field1_ru", "field2_eu", "field2_ru"]
            )
        ]

        self.models_invalid = [
            self.model("field", "field_eu"),
            self.model("field1", "field2"),
        ]

    @patch("garpix_page.utils.get_exclude_fields.get_languages")
    def test_get_exclude_fields(self, get_languages) -> None:
        get_languages.return_value = ["eu", "ru"]
        for model, return_ in self.models:
            self.assertEqual(
                get_exclude_fields(model),
                return_,
            )

    @patch("garpix_page.utils.get_exclude_fields.get_languages")
    def test_get_exclude_fields_invalid(self, get_languages) -> None:
        get_languages.return_value = ["eu", "ru"]
        for model in self.models_invalid:
            self.assertFalse(bool(get_exclude_fields(model)))
