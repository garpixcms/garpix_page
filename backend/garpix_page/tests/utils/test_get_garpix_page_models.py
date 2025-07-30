from typing import List, Type

import django.apps
from rest_framework.test import APITestCase

from garpix_page.models.base_page import BasePage
from garpix_page.models.components import BaseComponent
from garpix_page.utils.get_garpix_page_models import (
    get_garpix_page_models,
    get_garpix_page_component_models,
)


class GetGarpixPageModelsTest(APITestCase):
    def setUp(self) -> None:
        self.model_list = self.get_page_models()
        self.components_list = self.get_component_models()

    def test_get_garpix_page_models(self) -> None:
        pages = sorted(self.model_list, key=lambda x: x._meta.verbose_name)
        self.assertEqual(get_garpix_page_models(), pages)
    
    def test_get_garpix_page_component_models(self) -> None:
        pages = sorted(self.components_list, key=lambda x: x._meta.verbose_name)
        self.assertEqual(get_garpix_page_component_models(), pages)

    def get_page_models(self) -> List[Type[BasePage]]:
        model_list = []
        for model in django.apps.apps.get_models():
            try:
                if model.is_for_page_view() and model is not BasePage:
                    model_list.append(model)
            except:  # noqa
                pass
        return model_list
    
    def get_component_models(self) -> List[Type[BaseComponent]]:
        components_list = []
        for model in django.apps.apps.get_models():
            try:
                if model.is_for_component_view() and model is not BaseComponent:
                    components_list.append(model)
            except:  # noqa
                pass
        return components_list
