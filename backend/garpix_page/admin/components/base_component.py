from django.contrib import admin, messages
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.text import format_lazy
from modeltranslation.admin import TabbedTranslationAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter, PolymorphicChildModelAdmin

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import path
from garpix_page.models import BaseComponent, BasePage
from garpix_page.utils.get_garpix_page_models import get_garpix_page_component_models
from ..forms import PolymorphicModelPreviewChoiceForm, BaseComponentForm
from garpix_utils.logs.enums.get_enums import Action
from garpix_utils.logs.loggers import ib_logger
from garpix_utils.logs.mixins.create_log import CreateLogMixin


class BaseComponentAdmin(PolymorphicChildModelAdmin, TabbedTranslationAdmin, CreateLogMixin):
    base_model = BaseComponent
    base_form = BaseComponentForm
    list_display = ('title', 'model_name')
    search_fields = ('title', 'pages__title')

    filter_horizontal = (
        'pages',
    )

    change_form_template = 'garpix_page/admin/component_change_form.html'

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

    def get_form(self, request, obj=None, **kwargs):
        if request.GET.get('_popup') and request.GET.get('_to_field'):
            self.exclude = ('pages',)
        return super().get_form(request, obj=None, **kwargs)

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


@admin.register(BaseComponent)
class RealBaseComponentAdmin(PolymorphicParentModelAdmin, TabbedTranslationAdmin, CreateLogMixin):
    child_models = get_garpix_page_component_models()
    base_model = BaseComponent
    list_filter = (PolymorphicChildModelFilter, )
    add_type_form = PolymorphicModelPreviewChoiceForm
    save_on_top = True
    list_display = ('title', 'pages_list', 'model_name', 'is_active', 'is_deleted')
    search_fields = ('title', 'pages__title')
    list_editable = ('is_active',)
    actions = ('clone_object', 'soft_delete_queryset', 'restore_queryset')

    def get_actions(self, request):
        actions = super().get_actions(request)

        if actions is not None and "delete_selected" in actions:
            delete_selected = (
                actions["delete_selected"][0],
                actions["delete_selected"][1],
                "Удалить выбранные компоненты из базы данных",
            )
            del actions["delete_selected"]
            actions.update({
                'delete_selected': delete_selected
            })
        return actions

    def soft_delete_queryset(self, request, queryset):

        logs = []
        for obj in queryset:
            obj.is_deleted = True
            logs.append( self.log_change_or_create(ib_logger, request, obj, True))

        BaseComponent.objects.bulk_update(queryset, ['is_deleted'])

        for log in logs:
            ib_logger.write_string(log)

        messages.add_message(request, messages.SUCCESS, 'Компоненты отмечены как удаленные')

    soft_delete_queryset.short_description = 'Удалить выбранные компоненты'

    def pages_list(self, obj):
        pages = obj.pages.all()
        pages_str = ', '.join(pages[:6].values_list('title', flat=True))
        if (more_count := pages.count() - 6) > 0:
            pages_str += f' ...еще {more_count}'
        return pages_str

    pages_list.short_description = 'Страницы для отображения'

    def clone_object(self, request, queryset):
        """Копирование(клонирование) выбранных объектов - action"""
        for obj in queryset:

            obj = obj.get_real_instance()

            len_old_title = obj.__class__.objects.filter(title__icontains=obj.title).count()
            title = f"{obj.title} ({len_old_title})" if len_old_title > 0 else obj.title

            new_obj = obj.clone_object(title=title)

            new_obj.pages.set([])

            new_obj.save()

            log = self.log_change_or_create(ib_logger, request, new_obj, False)
            ib_logger.write_string(log)

    clone_object.short_description = 'Клонировать объект'

    def get_urls(self):
        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = [
            path('<path:pk>/full_clone/', self.full_clone, name='%s_%s_full_clone' % info),
        ]

        return my_urls + urls

    def full_clone(self, request, pk):
        if request.method == 'POST':
            obj = self.get_object(request, pk)

            obj = obj.get_real_instance()

            title = request.POST.get('title', None)

            if not title:
                len_old_title = obj.__class__.objects.filter(title__icontains=obj.title).count()
                title = f"{obj.title} ({len_old_title})" if len_old_title > 0 else obj.title

            new_obj = obj.clone_object(title=title)

            new_obj.pages.set([])

            new_obj.save()

            log = self.log_change_or_create(ib_logger, request, new_obj, False)
            ib_logger.write_string(log)

        link = reverse("admin:garpix_page_basecomponent_changelist")
        return HttpResponseRedirect(link)

    def restore_queryset(self, request, queryset):

        logs = []
        for obj in queryset:
            obj.is_deleted = False
            logs.append( self.log_change_or_create(ib_logger, request, obj, True))

        BaseComponent.objects.bulk_update(queryset, ['is_deleted'])

        for log in logs:
            ib_logger.write_string(log)

        messages.add_message(request, messages.SUCCESS, 'Компоненты восстановлены')

    restore_queryset.short_description = 'Восстановить выбранные компоненты'

    def get_deleted_objects(self, objs, request):
        """
        Hook for customizing the delete process for the delete view and the
        "delete selected" action.
        """
        to_delete, model_count, perms_needed, protected = [], {}, set(), []
        for obj in objs:
            _to_delete, _model_count, _perms_needed, _protected = super().get_deleted_objects([obj], request)
            to_delete.extend(_to_delete)
            model_count.update(_model_count)
            perms_needed.update(_perms_needed)
            protected.extend(_protected)
        return to_delete, model_count, perms_needed, protected

    def delete_queryset(self, request, queryset):
        action = Action.any_entity_delete.value
        logs = []
        for obj in queryset:
            logs.append(self.log_delete(ib_logger, request, obj, action))

        self.model.objects.filter(id__in=queryset.values_list('id', flat=True)).delete()

        for log in logs:
            ib_logger.write_string(log)
