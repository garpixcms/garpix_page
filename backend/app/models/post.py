from django.db import models
from garpix_page.models import BasePage


class Post(BasePage):
    content = models.TextField(verbose_name='Содержание', blank=True, default='')

    template = 'pages/default.html'

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ('-created_at',)
