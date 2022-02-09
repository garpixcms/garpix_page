from django.db import models
from .base_component import BaseComponent


class BaseTextDescriptionComponent(BaseComponent):
    text = models.TextField(verbose_name='Текст')
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    template = 'garpix_page/components/base_text_description.html'

    class Meta:
        abstract = True
