from django.contrib import admin
from django.utils.html import format_html

from ..models.base_page import BasePage
from modeltranslation.admin import TabbedTranslationAdmin
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin
from ..utils.get_garpix_page_models import get_garpix_page_models
from django.conf import settings
from django.utils.translation import gettext as _
from polymorphic.admin import PolymorphicChildModelFilter
from tabbed_admin import TabbedModelAdmin
from mptt.admin import DraggableMPTTAdmin


class BasePageAdmin(TabbedModelAdmin, TabbedTranslationAdmin, PolymorphicMPTTChildModelAdmin):
    base_model = BasePage

    list_per_page = settings.GARPIX_PAGE_ADMIN_LIST_PER_PAGE if hasattr(settings, 'GARPIX_PAGE_ADMIN_LIST_PER_PAGE') else 25
    change_form_template = 'garpix_page/admin/page_change_form.html'
    empty_value_display = '- нет -'
    save_on_top = True
    view_on_site = True

    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}

    search_fields = ('title',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    actions = ('clone_object', 'rebuild')

    list_display = ('title', 'created_at', 'is_active', 'get_absolute_url',)
    list_editable = ('is_active',)

    readonly_fields = ('created_at', 'updated_at')

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        # form.current_user = request.user
        return form

    def delete_queryset(self, request, queryset):
        self.model.objects.delete(id__in=queryset.values_list('id', flat=True))
        self.model.objects.rebuild()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions is not None and "delete_selected" in actions:
            actions["delete_selected"] = (
                self.delete_queryset,
                "delete_selected",
                _("Delete selected %(verbose_name_plural)s"),
            )
        return actions

    def has_module_permission(self, request):
        return False

    def get_fieldsets(self, request, obj=None):
        """
        Если в модели страницы определены табы, будут отображаться они.
        Если не определены - все доступные филдсеты/поля будут помещены в таб "Основное", сео теги - в таб "Сео"
        """
        if self.tabs is None:
            fields = self.get_fields(request, obj)
            tab_seo_fields = []
            tab_main_fields = []
            for field in fields:
                if field[:4] == 'seo_':
                    tab_seo_fields.append(field)
                else:
                    tab_main_fields.append(field)
            tab_seo = (
                (None, {
                    'fields': tab_seo_fields
                }),
            )

            if self.fieldsets:
                tab_main = self.fieldsets
            else:
                tab_main = (
                    (None, {
                        'fields': tab_main_fields
                    }),
                )

            self.tabs = [
                ('Основное', tab_main),
                ('SEO', tab_seo)
            ]
        tabs_fieldsets = self.get_formatted_tabs(request, obj)['fieldsets']
        self.fieldsets = ()
        self.fieldsets = self.add_tabbed_item(tabs_fieldsets, self.fieldsets)
        return super(BasePageAdmin, self).get_fieldsets(request, obj)


@admin.register(BasePage)
class RealBasePageAdmin(DraggableMPTTAdmin, TabbedTranslationAdmin, PolymorphicMPTTParentModelAdmin):
    """
    Стандартные настройки для базовых страниц.
    """
    base_model = BasePage
    child_models = get_garpix_page_models()

    list_per_page = settings.GARPIX_PAGE_ADMIN_LIST_PER_PAGE if hasattr(settings, 'GARPIX_PAGE_ADMIN_LIST_PER_PAGE') else 25

    empty_value_display = '- нет -'
    save_on_top = True
    view_on_site = True

    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}

    search_fields = ('title',)
    list_filter = (PolymorphicChildModelFilter, 'is_active', 'created_at', 'updated_at', 'sites')
    actions = ('clone_object', 'rebuild')

    list_display = ('tree_actions', 'indented_title', 'created_at', 'is_active', 'get_absolute_url_html_admin')
    list_editable = ('is_active',)

    readonly_fields = ('created_at', 'updated_at', 'model_name')

    def indented_title(self, item):
        return super(RealBasePageAdmin, self).indented_title(item)

    indented_title.short_description = "Название"

    def get_absolute_url_html_admin(self, obj):
        return format_html('<a href="{0}" target="_blank">{0}</a>', obj.absolute_url)

    get_absolute_url_html_admin.short_description = 'URL'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['parent'].queryset = self.model.get_available_page_parents()
            self.fields['parent'].default = self.model.get_default_parent()

    def clone_object(self, request, queryset):
        """Копирование(клонирование) выбранных объектов - action"""
        for obj in queryset:
            prefix = '-CLONE'
            clone = obj
            clone.title += prefix
            clone.slug += prefix
            clone.id = None
            clone.is_active = False
            clone.save()

    clone_object.short_description = 'Клонировать объект'

    def _rebuild(self):
        try:
            self.model.objects.rebuild()
        except:  # noqa
            print('[ERROR]: Ошибка при перезагрузки древовидной структуры')

    def rebuild(self, request, queryset):
        """Пересорбать МПТТ модель. Иногда требуется для перезагрузки дерева."""
        self._rebuild()

    rebuild.short_description = 'Пересобрать пункты раздела'

    def save_model(self, request, obj, form, change):
        self._rebuild()
        super().save_model(request, obj, form, change)
