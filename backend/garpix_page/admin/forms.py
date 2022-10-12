from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from polymorphic.admin import PolymorphicModelChoiceForm
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from polymorphic_tree.admin import PolymorpicMPTTAdminForm

from garpix_page.models import BasePage
from garpix_page.utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix

from django.db.models import CharField, TextField
from garpix_page.utils.get_garpix_page_models import get_garpix_page_models


class AdminRadioSelectPreview(forms.RadioSelect):
    template_name = 'garpix_page/admin/widgets/radio_preview.html'

    def create_option(self, name, value, *args, **kwargs):
        result = super().create_option(name, value, *args, **kwargs)
        ct = ContentType.objects.filter(pk=value).first()
        result['attrs']['preview'] = []
        result['attrs']['group'] = None
        if ct is not None:
            model = apps.get_model(ct.app_label, ct.model)
            preview = getattr(model, 'admin_preview_image', [])
            group = getattr(model, 'admin_group', None)
            result['attrs']['preview'] = preview if isinstance(preview, list) else [preview]
            result['attrs']['group'] = group
        return result

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["sorted_groups"] = self.sorted_groups(
            context["widget"]["optgroups"]
        )
        return context

    def sorted_groups(self, optgroups):
        groups = optgroups
        result = {}
        for group in groups:
            subgroups = group[1]
            for subgroup in subgroups:
                groupKey = subgroup['attrs']['group']
                if groupKey not in result:
                    result[groupKey] = []
                result[groupKey].append(subgroup)
        return result


class PolymorphicModelPreviewChoiceForm(PolymorphicModelChoiceForm):
    class Media:
        css = {
            'all': ('garpix_page/css/admin/styles.css',)
        }
        js = ('garpix_page/js/admin/components.js',)

    type_label = 'Тип'

    ct_id = forms.ChoiceField(
        label=type_label, widget=AdminRadioSelectPreview(attrs={"class": "radiolist"})
    )

    def __init__(self, *args, **kwargs):
        # Allow to easily redefine the label (a commonly expected usecase)
        super().__init__(*args, **kwargs)
        self.fields["ct_id"].label = self.type_label


class PageForm(PolymorpicMPTTAdminForm):
    def clean(self):
        cleaned_data = super().clean()

        sites = cleaned_data.get('sites')
        slug = cleaned_data.get('slug')
        parent = cleaned_data.get('parent')

        current_language_code_url_prefix = get_current_language_code_url_prefix()

        if slug:
            url_arr = [slug]
            if parent:
                obj = parent
                url_arr.insert(0, obj.slug)
                while obj.parent is not None:
                    obj = obj.parent
                    if obj.slug:
                        url_arr.insert(0, obj.slug)
            absolute_url = "{}/{}/".format(current_language_code_url_prefix, '/'.join(url_arr))
        else:
            absolute_url = "{}".format(current_language_code_url_prefix) if len(current_language_code_url_prefix) > 1 else '/'

        languages = [x[0] for x in settings.LANGUAGES]

        pages = BasePage.objects.filter(slug=slug).exclude(pk=self.instance.pk)

        for page in pages:
            if page.absolute_url == absolute_url and any(set(sites) & set(page.sites.all())):
                raise ValidationError({'slug': 'Страница с таким ЧПУ существует'})
        if slug in languages:
            raise ValidationError({'slug': f'ЧПУ не должен совпадать с языковым кодом ({languages})'})

        return cleaned_data


def get_model_rule_fields_values():
    model_rule_fields_values = []
    for page_model in get_garpix_page_models():
        model_rule_fields_values.append((page_model.__name__, page_model._meta.verbose_name))
    return model_rule_fields_values


def get_rule_fields_values():
    rule_fields_values = []
    for page_model in get_garpix_page_models():
        for f in page_model._meta.get_fields():
            if hasattr(f, 'verbose_name') and (isinstance(f, CharField) or isinstance(f, TextField)) and 'seo_' not in f.name and f.name != 'slug':
                prop_field = (f.name, f.verbose_name)
                if prop_field not in rule_fields_values:
                    rule_fields_values.append(prop_field)

        for f in [f for name in dir(page_model) if isinstance(f := getattr(page_model, name), cached_property)]:
            prop_field = (f.name, f.short_description)
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

    class Media:
        css = {
            'all': ('garpix_page/css/admin/seo_template.css',)
        }
        js = ('garpix_page/js/admin/seo_template.js',)
