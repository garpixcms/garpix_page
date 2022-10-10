from modeltranslation.admin import TabbedTranslationAdmin

from ..forms import SeoTemplateForm
from garpix_page.models import SeoTemplate

from django.contrib import admin


@admin.register(SeoTemplate)
class SeoTemplateAdmin(TabbedTranslationAdmin, admin.ModelAdmin):

    form = SeoTemplateForm

    list_display = ['__str__', 'priority_order']
