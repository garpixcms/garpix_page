from django.db import models
from garpix_utils.file import get_file_path

from .base_component import BasePageComponent


class SliderPageComponent(BasePageComponent):
    template = 'garpix_page/components/slider.html'

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдер"
        ordering = ('-created_at',)
