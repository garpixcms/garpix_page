from django.db import models

from garpix_page.models import BaseComponent


class TextComponent(BaseComponent):
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Текстовый компонент'
        verbose_name_plural = 'Текстовые компоненты'
