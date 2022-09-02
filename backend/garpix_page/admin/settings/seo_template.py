from django.contrib import admin
from django import forms
from django.db.models import CharField, TextField
from modeltranslation.admin import TabbedTranslationAdmin

from garpix_page.models import SeoTemplate


from garpix_page.utils.get_garpix_page_models import get_garpix_page_models


def get_model_rule_fields_values():
    model_rule_fields_values = []
    for page_model in get_garpix_page_models():
        model_rule_fields_values.append((page_model.__name__, page_model._meta.verbose_name))
    return model_rule_fields_values


def get_rule_fields_values():
    rule_fields_values = []
    for page_model in get_garpix_page_models():
        for f in page_model._meta.get_fields():
            if hasattr(f, 'verbose_name') and (isinstance(f, CharField) or isinstance(f, TextField)) and 'seo_' not in f.name:
                prop_field = (f.name, f.verbose_name)
                if prop_field not in rule_fields_values:
                    rule_fields_values.append(prop_field)
    return rule_fields_values


class SeoTemplateForm(forms.ModelForm):
    class RULE_FIELD:
        MODEL_NAME = 'model_name'

        CHOICES = (
            (MODEL_NAME, 'Название модели'),
        ) + tuple(get_rule_fields_values())

    rule_field = forms.ChoiceField(choices=RULE_FIELD.CHOICES)
    rule_field.label = 'Поле'
    model_rule_value = forms.ChoiceField(choices=tuple(get_model_rule_fields_values()))
    model_rule_value.label = 'Название'


@admin.register(SeoTemplate)
class SeoTemplateAdmin(TabbedTranslationAdmin, admin.ModelAdmin):

    form = SeoTemplateForm
