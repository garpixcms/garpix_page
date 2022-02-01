from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin, PolymorpicMPTTAdminForm
from ...utils.get_garpix_page_models import get_garpix_page_component_models
from django.conf import settings
from polymorphic.admin import PolymorphicChildModelFilter
from ...models import BasePageComponent


class BasePageComponentAdminForm(PolymorpicMPTTAdminForm):

    def clean(self):
        if self.cleaned_data["parent"] is None and len(self.cleaned_data["pages"]) == 0:
            raise ValidationError("Пожалуйста, выберите хотя бы одну страницу для отображения "
                                  "либо родительский компонент")

        if self.cleaned_data["parent"] is not None:
            self.cleaned_data["pages"] = []


class BasePageComponentAdmin(PolymorphicMPTTChildModelAdmin):
    base_model = BasePageComponent
    base_form = BasePageComponentAdminForm
    list_per_page = settings.GARPIX_PAGE_ADMIN_LIST_PER_PAGE if hasattr(settings, 'GARPIX_PAGE_ADMIN_LIST_PER_PAGE') else 25

    empty_value_display = '- нет -'
    save_on_top = True

    date_hierarchy = 'created_at'

    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')

    readonly_fields = ('created_at', 'updated_at')

    filter_vertical = (
        'pages',
    )

    def has_module_permission(self, request):
        return False

    class Media:
        js = ('garpix_page/components/admin/js/base_component.js',)


@admin.register(BasePageComponent)
class RealBasePageComponentAdmin(PolymorphicMPTTParentModelAdmin):

    base_model = BasePageComponent
    child_models = get_garpix_page_component_models()

    list_per_page = settings.GARPIX_PAGE_ADMIN_LIST_PER_PAGE if hasattr(settings, 'GARPIX_PAGE_ADMIN_LIST_PER_PAGE') else 25

    empty_value_display = '- нет -'

    date_hierarchy = 'created_at'

    search_fields = ('title',)
    list_filter = (PolymorphicChildModelFilter, 'created_at', 'updated_at')

    list_display = ('title', 'created_at', 'model_name')

    readonly_fields = ('created_at', 'updated_at', 'model_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['parent'].queryset = self.model.get_available_page_parents()
            self.fields['parent'].default = self.model.get_default_parent()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
