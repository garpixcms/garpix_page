from django.contrib import admin

from .base_component import BasePageComponentAdmin
from ...models import TextPageComponent, TextDescriptionPageComponent


@admin.register(TextDescriptionPageComponent)
class TextDescriptionPageComponentAdmin(BasePageComponentAdmin):
    pass
