import os
from django.conf import settings
from django.contrib import admin

__all__ = ('GrapesJsAdminMixin', )

from django.urls import path

from garpix_page.views.get_template import GetTemplate
from garpix_page.views.upload import DgjsUpload


class GrapesJsAdminMixin(admin.ModelAdmin):
    change_form_template = 'grapesjs/change_form.html'

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        obj.save()
        css = request.POST.get('html_css')
        js = request.POST.get('html_js')
        field_name = 'html'
        filename_css = f'{settings.MEDIA_ROOT}/grapesjs/{field_name}_{obj.pk}_css.css'
        filename_js = f'{settings.MEDIA_ROOT}/grapesjs/{field_name}_{obj.pk}_js.js'
        os.makedirs(os.path.dirname(filename_css), exist_ok=True)
        with open(filename_css, "w") as f:
            f.write(css)

        os.makedirs(os.path.dirname(filename_js), exist_ok=True)
        with open(filename_js, "w") as f:
            f.write(js)
        return obj

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('get_template/', GetTemplate.as_view(), name='dgjs_get_template'),
            path('dgjs_upload/', DgjsUpload.as_view(), name='dgjs_upload'),
        ]

        return my_urls + urls
