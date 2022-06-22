from django.contrib import admin

from garpix_page.admin.components.base_component import BaseComponentAdmin
from app.models import TextDescriptionComponent


@admin.register(TextDescriptionComponent)
class TextDescriptionComponentAdmin(BaseComponentAdmin):
    pass
