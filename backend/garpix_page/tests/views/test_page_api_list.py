from unittest.mock import patch
from typing import Type, List

from django.db.models import Model
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from garpix_page.utils.get_garpix_page_models import get_garpix_page_models


class PageApiListTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.models = self.create_page_models()
        self.validated_response = {
            model.__name__: model._meta.verbose_name
            for model in self.models
        }

    @patch("garpix_page.utils.get_garpix_page_models.get_garpix_page_models")
    def test_page_list(self, get_garpix_page_models) -> None:
        get_garpix_page_models.return_value = self.models
        
        response = self.client.get(f"/{settings.API_URL}/page_models_list/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.validated_response)
        self.assertEqual(get_garpix_page_models.called, True)

    def create_page_models(self) -> List[Type[object]]:
        models = []
        for i in range(3):
            models.append(
                type(
                    f"PageModel{i}",
                    (object,),
                    {
                        "url_patterns": (
                            lambda: {
                                "{model_name}": {
                                    "verbose_name": "{model_title}",
                                    "pattern": "",
                                },
                            }
                        ),
                        "_meta": type("_meta", (object,), {"verbose_name": f"page_model_{i}"})
                    }
                )
            )
        return models
