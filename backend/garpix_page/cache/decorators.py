from functools import wraps
from django.core.cache import caches
from django.utils.cache import _generate_cache_header_key


def cached_context(timeout, prefix=''):

    cache = caches['default']

    def _get_cache_key(function_name, obj, request, **kwargs):
        request_key = _generate_cache_header_key(prefix, request)
        arr = [function_name, request_key]
        # for key, value in kwargs.items():
        #     arr.extend([str(key), str(value)])
        return '{}:{}'.format(prefix, ':'.join(arr)).replace(' ', '_')

    def cached_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            cache_key = _get_cache_key(func.__name__, *args, **kwargs)

            cached_value = cache.get(cache_key)

            if cached_value is not None:
                return cached_value

            calculated_value = func(*args, **kwargs)

            cache.set(cache_key, calculated_value, timeout)
            return calculated_value

        return func_wrapper

    return cached_decorator
