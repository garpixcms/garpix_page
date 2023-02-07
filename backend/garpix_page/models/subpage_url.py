from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Manager

from garpix_page.utils.all_sites import get_all_sites
from django.contrib.sites.models import Site
from garpix_utils.managers import GCurrentSiteManager, ActiveOnSiteManager


class SubPageUrl(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Включено')
    pattern = models.CharField(max_length=100, verbose_name='pattern', help_text='Шаблон url, который будет добавлен после url страницы, к которой применяется')
    model_name = models.CharField(max_length=100, default='', verbose_name='Шаблон названия модели (ключ для фронта)', help_text='Ключ для подстановки названия модели - {model_name}')
    model_title = models.CharField(max_length=100, default='', verbose_name='Шаблон названия модели (для отображения)', help_text='Ключ для подстановки названия модели - {model_title}')
    sites = models.ManyToManyField(Site, default=get_all_sites, verbose_name='Сайты для отображения')
    sort = models.PositiveIntegerField(default=1, verbose_name='Порядок отображения')
    page_types = models.ManyToManyField(ContentType, blank=True, related_name='subpage_urls', verbose_name='Типы страниц для примeнения')

    objects = Manager()
    on_site = GCurrentSiteManager()
    active_on_site = ActiveOnSiteManager()

    params = None

    class Meta:
        verbose_name = 'Подстраница'
        verbose_name_plural = 'Подстраницы'
        ordering = ('-sort',)

    def __str__(self):
        return f'{self.id} - {self.get_pattern()}'

    def get_pattern(self):
        return f'{self.pattern}'

    def clean(self):
        super().clean()
        try:
            str(self.model_name).format(model_name='some_name')
        except KeyError:
            raise ValidationError({'model_name': 'Некорректный шаблон'})
        try:
            str(self.model_title).format(model_title='some_title')
        except KeyError:
            raise ValidationError({'model_title': 'Некорректный шаблон'})
