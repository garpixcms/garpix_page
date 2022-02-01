from polymorphic.admin import PolymorphicChildModelAdmin

from django.contrib import admin

from .base_component import BasePageComponentAdmin
from ...models import TextPageComponent, TextImagePageComponent, ImagePageComponent


@admin.register(ImagePageComponent)
class ImagePageComponentAdmin(BasePageComponentAdmin):
    pass
