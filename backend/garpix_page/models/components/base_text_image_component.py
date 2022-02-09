from django.db import models
from garpix_utils.file import get_file_path

from .base_component import BaseComponent


class BaseTextImageComponent(BaseComponent):
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(verbose_name='Изображение', upload_to=get_file_path)
    template = 'garpix_page/components/base_text_image.html'

    class Meta:
        abstract = True
