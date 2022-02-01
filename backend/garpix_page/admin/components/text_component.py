from django.contrib import admin

from .base_component import BasePageComponentAdmin
from ...models import TextPageComponent


@admin.register(TextPageComponent)
class TextPageComponentAdmin(BasePageComponentAdmin):
    pass
