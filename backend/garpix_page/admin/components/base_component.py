from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.text import format_lazy
from modeltranslation.admin import TabbedTranslationAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter, PolymorphicChildModelAdmin

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.urls import path
from garpix_page.models import BaseComponent, BasePage
from garpix_page.utils.get_garpix_page_models import get_garpix_page_component_models
from ..forms import PolymorphicModelPreviewChoiceForm


class BaseComponentAdmin(PolymorphicChildModelAdmin, TabbedTranslationAdmin):
    base_model = BaseComponent
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


@admin.register(BaseComponent)
class RealBaseComponentAdmin(PolymorphicParentModelAdmin, TabbedTranslationAdmin):
    child_models = get_garpix_page_component_models()
    base_model = BaseComponent
    list_filter = (PolymorphicChildModelFilter, )
    add_type_form = PolymorphicModelPreviewChoiceForm
    save_on_top = True
    list_display = ('title', 'pages_list', 'model_name', 'is_active')
    search_fields = ('title', 'pages__title')
    list_editable = ('is_active',)
    actions = ('clone_object', )

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
        link = reverse("admin:garpix_page_basecomponent_changelist")
        return HttpResponseRedirect(link)
