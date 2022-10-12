from django.db import models

from garpix_page.models import BasePage


class Page(BasePage):
    content = models.TextField(verbose_name='Содержание', blank=True, default='')

    template = 'pages/default.html'

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ('-created_at',)

    def get_seo_template_keys(self):
        seo_keys = super().get_seo_template_keys()
        seo_keys.update({
            'absolute_url': self.absolute_url
        })
        return seo_keys

    @classmethod
    def seo_template_keys_list(cls):
        return [('absolute_url', 'URL')]
