import django.apps
from ..models import BasePage, BasePageComponent, SliderPageComponent

model_list = []
components_list = []
components_admin_list = []

for model in django.apps.apps.get_models():
    try:
        if model.is_for_page_view() and model is not BasePage:
            model_list.append(model)
    except:  # noqa
        pass

for model in django.apps.apps.get_models():
    try:
        if model.is_for_component_view() and model is not BasePageComponent:
            components_list.append(model)
    except:  # noqa
        pass


from django.contrib import admin

models_list = []

for model, model_admin in admin.site._registry.items():
    try:
        if model.is_for_component_view() and model not in [BasePageComponent, SliderPageComponent]:
            components_admin_list.append(model_admin)
    except:  # noqa
        pass


def get_garpix_page_models():
    return model_list


def get_garpix_page_component_models():
    return components_list


def get_garpix_page_component_admin_models():
    return components_admin_list
