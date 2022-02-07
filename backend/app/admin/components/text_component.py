from django.contrib import admin

from garpix_page.admin.components.base_component import BasePageComponentAdmin
from ...models import TextPageComponent


@admin.register(TextPageComponent)
class TextPageComponentAdmin(BasePageComponentAdmin):
    pass
