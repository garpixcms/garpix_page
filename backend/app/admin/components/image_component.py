from django.contrib import admin

from garpix_page.admin.components.base_component import BaseComponentAdmin
from ...models import ImageComponent


@admin.register(ImageComponent)
class ImageComponentAdmin(BaseComponentAdmin):
    pass
