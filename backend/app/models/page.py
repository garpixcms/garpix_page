from django.db import models

from .. import serializers
from garpix_page.models import BasePage


class Page(BasePage):
    content = models.TextField(verbose_name='Содержание', blank=True, default='')

    template = 'pages/default.html'
    serializer = serializers.PageSerializer

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ('-created_at',)
