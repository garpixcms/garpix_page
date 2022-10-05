from django.contrib import admin
from .grepesjs_mixin import GrapesJsAdminMixin
from garpix_page.models import GrapesJsHtmlComponent
from .base_component import BaseComponentAdmin


@admin.register(GrapesJsHtmlComponent)
class GrapesJsHtmlComponentAdmin(BaseComponentAdmin, GrapesJsAdminMixin):
    pass
