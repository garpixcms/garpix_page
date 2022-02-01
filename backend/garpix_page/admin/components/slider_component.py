from django.contrib import admin

from .base_component import BasePageComponentAdmin
from ...models import TextPageComponent, SliderPageComponent, BasePageComponent
from polymorphic.admin import StackedPolymorphicInline


@admin.register(SliderPageComponent)
class SliderPageComponentAdmin(BasePageComponentAdmin):
    pass
