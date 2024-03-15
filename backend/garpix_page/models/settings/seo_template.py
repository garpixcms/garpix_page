from django.contrib.sites.models import Site
from django.db import models
from garpix_utils.file import get_file_path
from django.utils.translation import gettext as _
from garpix_utils.managers import GCurrentSiteManager
from garpix_utils.models import ActiveMixin

from garpix_page.utils.all_sites import get_all_sites
from garpix_page.cache import cache_service


class SeoTemplate(ActiveMixin, models.Model):
    rule_field = models.CharField(verbose_name=_('Поле'), max_length=255)

    model_rule_value = models.CharField(verbose_name=_('Название'), null=True, blank=True, max_length=255)
    rule_value = models.CharField(verbose_name=_('Значение'), null=True, blank=True, max_length=255)

    seo_title = models.CharField(max_length=250, verbose_name=_('SEO заголовок страницы (title)'), blank=True,
                                 default='')
    seo_keywords = models.CharField(max_length=250, verbose_name=_('SEO ключевые слова (keywords)'), blank=True,
                                    default='')
    seo_description = models.TextField(verbose_name=_('SEO описание (description)'), blank=True, default='')
    seo_author = models.CharField(max_length=250, verbose_name=_('SEO автор (author)'), blank=True, default='')
    seo_og_type = models.CharField(max_length=250, verbose_name=_('SEO og:type'), blank=True, default="website")
    seo_image = models.FileField(upload_to=get_file_path, blank=True, null=True, verbose_name=_('SEO изображение'))

    priority_order = models.PositiveIntegerField(default=1, help_text=_('Чем меньше число, тем выше приоритет'),
                                                 verbose_name=_('Приоритетность применения'))
    sites = models.ManyToManyField(Site, default=get_all_sites, verbose_name='Сайты для применения')

    objects = models.Manager()
    on_site = GCurrentSiteManager()

    class Meta:
        verbose_name = 'Шаблон для seo | SEO template'
        verbose_name_plural = 'Шаблоны для seo | SEO templates'
        ordering = ['priority_order', 'id']

    def __str__(self):
        return f'Шаблон для seo # {self.id}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        cache_service.clear_seo_data()
