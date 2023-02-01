from django.db import models
from garpix_page.utils.all_sites import get_all_sites
from django.contrib.sites.models import Site
from garpix_utils.managers import GCurrentSiteManager
from .base_page import BasePage
from django.utils.functional import cached_property


class HookPage(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Включено')
    pattern = models.CharField(max_length=100, verbose_name='pattern')
    model_name = models.CharField(max_length=100, default='', verbose_name='Model name')
    sites = models.ManyToManyField(Site, default=get_all_sites, verbose_name='Сайты для отображения')
    base_page = models.ForeignKey(BasePage, related_name='hook_pages', on_delete=models.CASCADE, verbose_name='Базовая страница')
    sort = models.PositiveIntegerField(default=1, verbose_name='Порядок отображения')

    on_site = GCurrentSiteManager()

    params = None

    class Meta:
        verbose_name = 'HookPage'
        verbose_name_plural = 'HookPages'
        ordering = ('-sort',)

    def __str__(self):
        return f'{self.id} - {self.get_pattern()}'

    def has_permission_required(self, request):
        return self.base_page.has_permission_required(request)

    @cached_property
    def root_page(self):
        params = self.params
        print(params, 'params')
        page_slug = params.get('page_slug')
        return BasePage.objects.filter(slug=page_slug).first()

    def get_context(self, request=None, *args, **kwargs):
        return {
            'object': self.root_page,
            'menu': []
        }

    def get_model_name(self):
        return self.model_name

    def get_pattern(self):
        return f'{self.pattern}'
