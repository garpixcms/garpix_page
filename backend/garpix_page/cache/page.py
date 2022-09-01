from django.core.cache import cache


class PageCacheService:
    cache_url_prefix = 'url_page_'
    cache_slug_prefix = 'slug_page_'

    def get_url(self, pk, current_language_code_url_prefix):
        cache_key = f'{self.cache_url_prefix}{pk}_{current_language_code_url_prefix}'
        url_cache = cache.get(cache_key)
        if url_cache is not None:
            return url_cache
        return None

    def set_url(self, pk, result):
        cache_key = f'{self.cache_url_prefix}{pk}'
        cache.set(cache_key, result)

    def get_instance_by_url(self, url):
        cache_key = f'{self.cache_slug_prefix}{url}'
        url_cache = cache.get(cache_key)
        if url_cache is not None:
            return url_cache
        return None

    def set_instance_by_url(self, url, result):
        cache_key = f'{self.cache_slug_prefix}{url}'
        cache.set(cache_key, result)

    def clear_all_by_page(self, pk, slug):
        cache.delete(f'{self.cache_url_prefix}{pk}')
        cache.delete(f'{self.cache_slug_prefix}{slug}')

    def clear_all(self):
        cache.clear()


cache_service = PageCacheService()
