from django.contrib import admin

from garpix_page.admin.components.base_component import BasePageComponentAdmin
from ...models import ImagePageComponent


@admin.register(ImagePageComponent)
class ImagePageComponentAdmin(BasePageComponentAdmin):
    pass
