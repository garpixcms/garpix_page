import django.apps
from ..models import BasePage


model_list = []
for model in django.apps.apps.get_models():
    try:
        if model.is_for_page_view() and model is not BasePage:
            model_list.append(model)
    except:  # noqa
        pass


def get_garpix_page_models():
    return model_list
