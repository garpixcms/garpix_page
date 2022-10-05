from django.db.models.signals import post_delete
from django.dispatch import receiver

from garpix_page.cache import cache_service

from garpix_page.models import SeoTemplate


@receiver(post_delete, sender=SeoTemplate)
def clean_seo_cache(sender, *args, **kwargs):
    cache_service.clear_seo_data()
