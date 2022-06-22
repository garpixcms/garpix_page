from django.contrib import admin

from garpix_page.admin.components.base_component import BaseComponentAdmin
from app.models import TextComponent


@admin.register(TextComponent)
class TextComponentAdmin(BaseComponentAdmin):
    pass
