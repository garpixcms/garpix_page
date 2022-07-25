from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.text import format_lazy
from modeltranslation.admin import TabbedTranslationAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter, PolymorphicChildModelAdmin

from garpix_page.models import BaseComponent, BasePage
from garpix_page.utils.get_garpix_page_models import get_garpix_page_component_models
from ..forms import PolymorphicModelPreviewChoiceForm


class BaseComponentAdmin(PolymorphicChildModelAdmin, TabbedTranslationAdmin):
    base_model = BaseComponent
    list_display = ('title', 'model_name')

    filter_horizontal = (
        'pages',
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.name == 'pages':
            kwargs['widget'] = FilteredSelectMultiple(
                db_field.verbose_name, is_stacked=False
            )
        else:
            return super().formfield_for_manytomany(db_field, request, **kwargs)
        if 'queryset' not in kwargs:
            queryset = BasePage.objects.all()
            if queryset is not None:
                kwargs['queryset'] = queryset
        form_field = db_field.formfield(**kwargs)
        msg = 'Hold down “Control”, or “Command” on a Mac, to select more than one.'
        help_text = form_field.help_text
        form_field.help_text = (
            format_lazy('{} {}', help_text, msg) if help_text else msg
        )
        return form_field

    def has_module_permission(self, request):
        return False


@admin.register(BaseComponent)
class RealBaseComponentAdmin(PolymorphicParentModelAdmin, TabbedTranslationAdmin):

    child_models = get_garpix_page_component_models()
    base_model = BaseComponent
    list_filter = (PolymorphicChildModelFilter, 'pages')
    list_display = ('title', 'model_name')
    add_type_form = PolymorphicModelPreviewChoiceForm
