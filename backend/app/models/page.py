from django.db import models
from garpix_page.models import BasePage


class Page(BasePage):
    content = models.TextField(verbose_name='Содержание', blank=True, default='')

    template = 'pages/default.html'

    login_required = True

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ('-created_at',)

    def user_has_permission_required(self, user):
        return user.is_superuser
