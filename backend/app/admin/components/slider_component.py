from django.contrib import admin

from garpix_page.admin.components.base_component import BaseComponentAdmin
from ...models import SliderComponent


@admin.register(SliderComponent)
class SliderComponentAdmin(BaseComponentAdmin):
    pass
