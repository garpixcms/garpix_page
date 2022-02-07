from django.contrib import admin

from garpix_page.admin.components.base_component import BasePageComponentAdmin
from ...models import SliderPageComponent


@admin.register(SliderPageComponent)
class SliderPageComponentAdmin(BasePageComponentAdmin):
    pass
