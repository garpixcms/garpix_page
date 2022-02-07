from django.contrib import admin

from garpix_page.admin.components.base_component import BasePageComponentAdmin
from ...models import TextImagePageComponent


@admin.register(TextImagePageComponent)
class TextImagePageComponentAdmin(BasePageComponentAdmin):
    pass
