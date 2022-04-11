from django.db import models

from garpix_page.models import BaseComponent


class TextDescriptionComponent(BaseComponent):
    text = models.TextField(verbose_name='Текст')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Компонент текст+описание'
        verbose_name_plural = 'Компоненты текст+описание'
