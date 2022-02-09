from django.db import models
from .base_component import BaseComponent


class BaseTextComponent(BaseComponent):
    text = models.TextField(verbose_name='Текст')
    template = 'garpix_page/components/base_text.html'

    class Meta:
        abstract = True
