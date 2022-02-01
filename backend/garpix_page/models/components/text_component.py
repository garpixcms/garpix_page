from django.db import models
from .base_component import BasePageComponent


class TextPageComponent(BasePageComponent):
    text = models.TextField(verbose_name='Текст')
    template = 'garpix_page/components/text.html'

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Текст"
        ordering = ('-created_at',)
