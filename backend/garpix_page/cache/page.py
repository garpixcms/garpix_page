from django.conf import settings
from django.core.cache import cache

from garpix_page.utils.all_sites import get_all_sites


class PageCacheService:
    cache_url_prefix = 'url_page_'
    cache_instance_prefix = 'instance_page_'

    def get_url(self, pk, current_language_code_url_prefix):
        current_site = getattr(settings, 'SITE_ID', 1)
        cache_key = f'{self.cache_url_prefix}{pk}_{current_site}_{current_language_code_url_prefix}'
        url_cache = cache.get(cache_key)
        if url_cache is not None:
            return url_cache
        return None

    def set_url(self, pk, current_language_code_url_prefix, result):
        current_site = getattr(settings, 'SITE_ID', 1)
        cache_key = f'{self.cache_url_prefix}{pk}_{current_site}_{current_language_code_url_prefix}'
        cache.set(cache_key, result)

    def get_instance_by_url(self, url):
        current_site = getattr(settings, 'SITE_ID', 1)
        cache_key = f'{self.cache_instance_prefix}_{current_site}_{url}'
        url_cache = cache.get(cache_key)
        if url_cache is not None:
            return url_cache
        return None

    def set_instance_by_url(self, url, result):
        current_site = getattr(settings, 'SITE_ID', 1)
        cache_key = f'{self.cache_instance_prefix}_{current_site}_{url}'
        cache.set(cache_key, result)

    def set_seo_by_page(self, pk, field_name, result, site):
        cache_key = f'page_{field_name}_{site}_{pk}'
        cache.set(cache_key, result)

    def get_seo_by_page(self, pk, field_name, site):
        cache_key = f'page_{field_name}_{site}_{pk}'
        seo_cache = cache.get(cache_key)
        if seo_cache is not None:
            return seo_cache
        return None

    def clear_seo_data(self, pk=None):
        from garpix_page.models import BasePage
        seo_fields = [field_name for field in BasePage._meta.get_fields() if (field_name := field.name)[:4] == 'seo_']
        keys = []
        if pk:
            for seo_field in seo_fields:
                for site in get_all_sites():
                    keys.append(f'page_{seo_field}_{site}_{pk}')
        else:
            for page in BasePage.objects.all():
                for seo_field in seo_fields:
                    for site in get_all_sites():
                        keys.append(f'page_{seo_field}_{site}_{page.pk}')

        cache.delete_many(keys=keys)

    def clear_all_by_page(self, instance, current_language_code_url_prefix):
        url, pk = instance.get_absolute_url(), instance.pk
        cache.delete(f'{self.cache_url_prefix}{pk}_{current_language_code_url_prefix}')
        cache.delete(f'{self.cache_instance_prefix}{url}')
        self.clear_seo_data(pk)

    def reset_url_info_by_page(self, instance, current_language_code_url_prefix):
        pk, old_url = instance.pk, instance.get_absolute_url()
        current_site = getattr(settings, 'SITE_ID', 1)
        url_cache_key = f'{self.cache_url_prefix}{pk}_{current_site}_{current_language_code_url_prefix}'
        instance_cache_key = f'{self.cache_instance_prefix}_{current_site}_{old_url}'
        cache.delete(url_cache_key)
        cache.delete(instance_cache_key)

        new_url = instance.get_absolute_url()
        self.set_instance_by_url(new_url, instance)

    def clear_all(self):
        cache.clear()


cache_service = PageCacheService()
