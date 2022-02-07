from django.db import models
from .base_component import BasePageComponent


class BaseTextPageComponent(BasePageComponent):
    text = models.TextField(verbose_name='Текст')
    template = 'garpix_page/components/text.html'

    class Meta:
        abstract = True
