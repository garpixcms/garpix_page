from django.contrib import admin
from django import forms
from ..models.base_page import BasePage
from modeltranslation.admin import TabbedTranslationAdmin
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin, PolymorpicMPTTAdminForm
from ..utils.get_garpix_page_models import get_garpix_page_models


class BasePageAdmin(TabbedTranslationAdmin, PolymorphicMPTTChildModelAdmin):
    base_model = BasePage

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


@admin.register(BasePage)
class RealBasePageAdmin(TabbedTranslationAdmin, PolymorphicMPTTParentModelAdmin):
    """
    Стандартные настройки для базовых страниц.
    """
    base_model = BasePage
    child_models = get_garpix_page_models()

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
