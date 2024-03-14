import json

from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.template.response import TemplateResponse
from django.utils.html import format_html
from garpix_utils.logs.enums.get_enums import Action
from garpix_utils.logs.loggers import ib_logger
from garpix_utils.logs.mixins.create_log import CreateLogMixin

from .forms import PageForm
from ..models.base_page import BasePage
from modeltranslation.admin import TabbedTranslationAdmin
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import path

from ..models.components.base_component import PageComponent
from ..utils.all_sites import get_all_sites
from ..utils.get_garpix_page_models import get_garpix_page_models
from django.conf import settings
from django.utils.translation import gettext as _
from polymorphic.admin import PolymorphicChildModelFilter
from tabbed_admin.admin import TabbedModelAdmin
from mptt.admin import DraggableMPTTAdmin
from garpix_admin_lock.mixins import PageLockAdminMixin

from ..utils.get_languages import get_languages
from ..views.clear_cache import clear_cache


class ComponentsTabularInline(admin.TabularInline):
    model = PageComponent
    fields = ('component', 'view_order')
    raw_id_fields = ('component',)
    extra = 0


class PageAdmin(TabbedModelAdmin, TabbedTranslationAdmin, PolymorphicMPTTChildModelAdmin, CreateLogMixin):
    base_model = BasePage
    list_per_page = settings.GARPIX_PAGE_ADMIN_LIST_PER_PAGE if hasattr(settings,
                                                                        'GARPIX_PAGE_ADMIN_LIST_PER_PAGE') else 25
    empty_value_display = '- нет -'
    save_on_top = True
    view_on_site = True

    base_form = PageForm

    change_form_template = 'garpix_page/admin/page_change_form.html'

    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}

    search_fields = ('title',)
    list_filter = ('is_active', 'created_at', 'updated_at')
    actions = ('clone_object', 'rebuild')

    list_display = ('title', 'created_at', 'is_active', 'url',)
    list_editable = ('is_active',)
    raw_id_fields = ('parent',)

    readonly_fields = ('url', 'created_at', 'updated_at')

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        obj = args[0]

        if obj and isinstance(obj, BasePage):
            sites = obj.sites.all() if obj.sites else get_all_sites()
            lang_seo_fields = ['seo_title', 'seo_keywords', 'seo_description', 'seo_author']
            non_lang_seo_fields = ['seo_og_type', 'seo_image']
            for field in non_lang_seo_fields:
                form.base_fields[field].help_text = "Итоговое значение:"
                for site in sites:
                    form.base_fields[field].help_text += f"<br> для сайта {site.name} - {obj.get_seo_value(field_name=field, site=site)}"

            for field in lang_seo_fields:
                for lang in get_languages():
                    lang = lang.replace('-', '_')
                    form.base_fields[f'{field}_{lang}'].help_text = "Итоговое значение:"
                    for site in sites:
                        form.base_fields[f'{field}_{lang}'].help_text += f"<br> для сайта {site.name} - {obj.get_seo_value(field_name=f'{field}_{lang}', site=site)}"

        # form.current_user = request.user
        return form

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

            if self.inlines:
                tab_main += tuple(self.inlines)

            self.tabs = [
                ('Основное', tab_main),
                ('SEO', tab_seo),
                ('Компоненты', (ComponentsTabularInline,))
            ]

        tabs_fieldsets = self.get_formatted_tabs(request, obj)['fieldsets']
        self.fieldsets = ()
        self.fieldsets = self.add_tabbed_item(tabs_fieldsets, self.fieldsets)

        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        log = self.log_change_or_create(ib_logger, request, obj, change)
        super().save_model(request, obj, form, change)
        ib_logger.write_string(log)

    def save_related(self, request, form, formsets, change):
        if change:
            log = self.log_change_m2m_field(ib_logger, request, super(), form, formsets, change,
                                            action_change=Action.any_entity_change.value)
            if log:
                ib_logger.write_string(log)
        else:
            super().save_related(request, form, formsets, change)

    def delete_model(self, request, obj):
        action = Action.any_entity_delete.value
        log = self.log_delete(ib_logger, request, obj, action)
        super().delete_model(request, obj)
        ib_logger.write_string(log)

    def delete_queryset(self, request, queryset):
        action = Action.any_entity_delete.value
        logs = []
        for obj in queryset:
            logs.append(self.log_delete(ib_logger, request, obj, action))

        self.model.objects.filter(id__in=queryset.values_list('id', flat=True)).delete()

        for log in logs:
            ib_logger.write_string(log)

        self.model.objects.rebuild()


@admin.register(BasePage)
class RealPageAdmin(DraggableMPTTAdmin, TabbedTranslationAdmin, PolymorphicMPTTParentModelAdmin, CreateLogMixin):
    """
    Стандартные настройки для базовых страниц.
    """
    base_model = BasePage
    child_models = get_garpix_page_models()

    list_per_page = settings.GARPIX_PAGE_ADMIN_LIST_PER_PAGE if hasattr(settings,
                                                                        'GARPIX_PAGE_ADMIN_LIST_PER_PAGE') else 25

    empty_value_display = '- нет -'
    save_on_top = True
    view_on_site = True

    date_hierarchy = 'created_at'
    prepopulated_fields = {'slug': ('title',)}

    search_fields = ('title',)
    list_filter = (PolymorphicChildModelFilter, 'is_active', 'created_at', 'updated_at', 'sites')
    actions = ('clone_object', 'rebuild')

    list_display = ('tree_actions', 'indented_title', 'created_at', 'is_active',
                    'get_absolute_url_html_admin', 'model_name')
    list_editable = ('is_active',)

    readonly_fields = ('created_at', 'updated_at', 'model_name')

    def delete_queryset(self, cls, request, queryset):
        action = Action.any_entity_delete.value
        logs = []
        for obj in queryset:
            logs.append(self.log_delete(ib_logger, request, obj, action))

        self.model.objects.filter(id__in=queryset.values_list('id', flat=True)).delete()

        for log in logs:
            ib_logger.write_string(log)

        self.model.objects.rebuild()

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions is not None and "delete_selected" in actions:
            actions["delete_selected"] = (
                self.delete_queryset,
                "delete_selected",
                _("Удалить выбранные %(verbose_name_plural)s"),
            )
        return actions

    def indented_title(self, item):
        return super().indented_title(item)

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
            obj = obj.get_real_instance()

            len_old_title = obj.__class__.objects.filter(title__icontains=obj.title).count()
            title = f"{obj.title} ({len_old_title})"
            slug = f"{obj.slug}-{len_old_title}"
            obj.title = title
            obj.slug = slug
            new_obj = obj.clone_object(title=title, slug=slug)
            new_obj.save()

            log = self.log_change_or_create(ib_logger, request, new_obj, False)
            ib_logger.write_string(log)

    clone_object.short_description = 'Клонировать объект'

    def _rebuild(self):
        try:
            self.model.objects.rebuild()
        except:  # noqa
            print('[ERROR]: Ошибка при перезагрузке древовидной структуры')

    def rebuild(self, request, queryset):
        """Пересорбать МПТТ модель. Иногда требуется для перезагрузки дерева."""
        self._rebuild()

    rebuild.short_description = 'Пересобрать пункты раздела'

    def save_model(self, request, obj, form, change):
        self._rebuild()
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = [
            path('<path:pk>/full_clone/', self.full_clone, name='%s_%s_full_clone' % info),
            path('admin_clear_cache', clear_cache, name='admin_clear_cache')
        ]

        return my_urls + urls

    def full_clone(self, request, pk):
        if request.method == 'POST':
            obj = self.get_object(request, pk)
            obj = obj.get_real_instance()
            title = request.POST.get('title', None)
            len_old_title = obj.__class__.objects.filter(title__icontains=obj.title).count()
            if not title:
                title = f"{obj.title} ({len_old_title})" if len_old_title > 0 else obj.title
            slug = f"{obj.slug}-{len_old_title}"
            new_obj = obj.clone_object(title=title, slug=slug)
            new_obj.save()

            log = self.log_change_or_create(ib_logger, request, new_obj, False)
            ib_logger.write_string(log)
        link = reverse("admin:garpix_page_basepage_changelist")
        return HttpResponseRedirect(link)


#  Базовая админка для страниц с локом
class BasePageAdmin(PageLockAdminMixin, PageAdmin):
    lock_change_view = True
    change_form_template = 'garpix_page/admin/page_change_form.html'

    def get_model_perms(self, request):
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request),
        }

    def has_change_permission(self, req, *args):
        can_add = super().has_change_permission(req, *args)

        if can_add and not self._is_locked(req):
            return True

        return False

    def _response_post_save_page(self, request):
        url = request.build_absolute_uri()
        _meta = self.model._meta
        model_name = _meta.model_name
        if model_name in url:
            return True, HttpResponseRedirect(reverse(f'admin:{_meta.app_label}_{_meta.model_name}_changelist'))
        return False, None

    def response_post_save_add(self, request, obj):
        res, response = self._response_post_save_page(request)
        if res:
            return response
        return self._get_parent_admin().response_post_save_add(request, obj)

    def response_post_save_change(self, request, obj):
        res, response = self._response_post_save_page(request)
        if res:
            return response
        return self._get_parent_admin().response_post_save_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):

        opts = self.model._meta

        if IS_POPUP_VAR in request.POST:
            popup_response_data = json.dumps({
                'action': 'delete',
                'value': str(obj_id),
            })
            return TemplateResponse(request, self.popup_response_template or [
                'admin/%s/%s/popup_response.html' % (opts.app_label, opts.model_name),
                'admin/%s/popup_response.html' % opts.app_label,
                'admin/popup_response.html',
            ], {
                'popup_response_data': popup_response_data,
            })

        self.message_user(
            request,
            _('The %(name)s “%(obj)s” was deleted successfully.') % {
                'name': opts.verbose_name,
                'obj': obj_display,
            },
            messages.SUCCESS,
        )

        res, response = self._response_post_save_page(request)
        if res:
            return response
        return self._get_parent_admin().response_delete(request, obj_display, obj_id)


class RealBasePageAdmin(PageLockAdminMixin, RealPageAdmin):
    lock_change_view = True


#  Базовая админка для страниц без лока
class RealBasePageWithoutLockAdmin(PageAdmin):
    pass


class BasePageWithoutLockAdmin(PageAdmin):
    pass
