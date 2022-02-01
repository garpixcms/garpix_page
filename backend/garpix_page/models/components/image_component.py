from django.db import models
from garpix_utils.file import get_file_path

from .base_component import BasePageComponent


class ImagePageComponent(BasePageComponent):
    image = models.ImageField(verbose_name='Изображение', upload_to=get_file_path)
    template = 'garpix_page/components/image.html'

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображение"
        ordering = ('-created_at',)
