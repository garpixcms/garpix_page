from django.db import models
from garpix_utils.models import GarpixSiteConfiguration


class GarpixPageSiteConfiguration(GarpixSiteConfiguration):
    class CHANGEFRAQ:
        ALWAYS = 'always'
        HOURLY = 'hourly'
        DAILY = 'daily'
        WEEKLY = 'weekly'
        MONTHLY = 'monthly'
        YEARLY = 'yearly'
        NEVER = 'never'

        CHOICES = (
            (ALWAYS, 'always'),
            (HOURLY, 'hourly'),
            (DAILY, 'daily'),
            (WEEKLY, 'weekly'),
            (MONTHLY, 'monthly'),
            (YEARLY, 'yearly'),
            (NEVER, 'never')
        )

    robots_txt = models.TextField(verbose_name='Содержимое файла robots.txt',
                                  default="User-agent: *\nDisallow: /admin/\nDisallow: /api/")
    sitemap_frequency = models.CharField(max_length=7, choices=CHANGEFRAQ.CHOICES, default=CHANGEFRAQ.ALWAYS,
                                         verbose_name='Sitemap changefreq')

    class Meta:
        verbose_name = 'Настройки | Settings'
        verbose_name_plural = 'Настройки | Settings'
