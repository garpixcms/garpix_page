import re

from django.urls.resolvers import RoutePattern, _route_to_regex

from garpix_page.cache import cache_service
from garpix_page.utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix
from django.utils.translation import activate

from garpix_page.utils.get_garpix_page_models import get_garpix_page_models


class PageViewMixin:

    @staticmethod
    def get_absolute_url_from_request(slug_list, slug):
        current_language_code_url_prefix = get_current_language_code_url_prefix()
        if slug != '':
            return "{}/{}".format(current_language_code_url_prefix, '/'.join(slug_list))
        return "{}".format(current_language_code_url_prefix) if len(current_language_code_url_prefix) > 1 else '/'

    @classmethod
    def get_instance_by_slug(cls, slugs, languages_list):
        slug_list = slugs.split('/')

        lang = None

        if slug_list[0] in languages_list:
            lang = slug_list.pop(0)
            activate(lang)

        if len(slug_list) == 0:
            slug_list.append('')

        if len(slug_list) > 1 and slug_list[-1] == '':
            slug_list.pop(-1)

        slug = slug_list[-1]

        url = cls.get_absolute_url_from_request(slug_list, slug)

        instance_cache = cache_service.get_instance_by_url(url)

        if instance_cache is not None:
            return instance_cache

        page_models = get_garpix_page_models()
        active_models = []
        for el in page_models:
            for key, value in el.url_patterns().items():
                pattern = RoutePattern(r'(<url>){}'.format(value['pattern']))
                pattern.regex = re.compile('^/(?P<url>.*){}$'.format(_route_to_regex(value['pattern'], pattern._is_endpoint)[0][1:]))
                match = pattern.match(url)
                if match is not None:
                    last, _, params = match

                    el_url = f"/{params['url']}"
                    el_slug = '' if lang and params['url'] == lang else el_url.split('/')[-1]

                    active_models.append({
                        'model': el,
                        'params': params,
                        'pattern': key,
                        'url': el_url,
                        'slug': el_slug
                    })

        for model in active_models:
            instances = model['model'].active_on_site.filter(slug=model['slug']).all()

            for instance in instances:

                if instance.absolute_url == model['url']:
                    instance.subpage_params = model['params']
                    instance.subpage_key = model['pattern']
                    cache_service.set_instance_by_url(url, instance)
                    return instance

        return None
