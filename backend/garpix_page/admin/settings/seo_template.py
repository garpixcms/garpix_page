from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin

from ..forms import SeoTemplateForm
from garpix_page.models import SeoTemplate

from django.contrib import admin


@admin.register(SeoTemplate)
class SeoTemplateAdmin(TabbedTranslationAdmin, admin.ModelAdmin):

    form = SeoTemplateForm

    list_display = ['__str__', 'priority_order']

    readonly_fields = ('get_seo_template_keys', )

    def get_seo_template_keys(self, obj):
        from garpix_page.utils.get_garpix_page_models import get_garpix_page_models
        seo_template_keys_field = ''
        seo_template_keys = []
        for page_model in get_garpix_page_models():
            for field in page_model.seo_template_keys_list():
                if field[0] not in seo_template_keys:
                    seo_template_keys.append(field[0])
                    seo_template_keys_field += f'<b>{field[0]}</b> ({field[1]})</br>'
        return format_html(seo_template_keys_field)

    get_seo_template_keys.short_description = 'Доступные ключи'
