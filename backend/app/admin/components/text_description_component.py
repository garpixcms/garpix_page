from django.contrib import admin

from garpix_page.admin.components.base_component import BasePageComponentAdmin
from ...models import TextDescriptionPageComponent


@admin.register(TextDescriptionPageComponent)
class TextDescriptionPageComponentAdmin(BasePageComponentAdmin):
    pass
