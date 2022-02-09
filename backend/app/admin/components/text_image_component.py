from django.contrib import admin

from garpix_page.admin.components.base_component import BaseComponentAdmin
from ...models import TextImageComponent


@admin.register(TextImageComponent)
class TextImageComponentAdmin(BaseComponentAdmin):
    pass
