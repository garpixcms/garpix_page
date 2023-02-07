import re

from garpix_page.cache import cache_service
from garpix_page.models import BasePage, SubPageUrl
from garpix_page.utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix
from django.utils.translation import activate
from django.urls.resolvers import RoutePattern, _route_to_regex


class PageViewMixin:

    @staticmethod
    def get_absolute_url_from_request(slug_list, slug):
        current_language_code_url_prefix = get_current_language_code_url_prefix()
        if slug != '':
            return "{}/{}".format(current_language_code_url_prefix, '/'.join(slug_list))
        return "{}".format(current_language_code_url_prefix) if len(current_language_code_url_prefix) > 1 else '/'

    @classmethod
    def get_instance_by_slug(cls, slugs, languages_list):
        subpage_urls = SubPageUrl.active_on_site.all()
        slug_list = slugs.split('/')

        if slug_list[0] in languages_list:
            activate(slug_list[0])
            slug_list.pop(0)

        if len(slug_list) == 0:
            slug_list.append('')

        if len(slug_list) > 1 and slug_list[-1] == '':
            slug_list.pop(-1)

        slug = slug_list[-1]

        url = cls.get_absolute_url_from_request(slug_list, slug)

        instance_cache = cache_service.get_instance_by_url(url)

        if instance_cache is not None:
            return instance_cache
        subpage_url = None
        for el in subpage_urls:
            pattern = RoutePattern(r'(<url>)/{}'.format(el.get_pattern()))
            pattern.regex = re.compile('^/(?P<url>.*)/{}'.format(_route_to_regex(el.get_pattern(), pattern._is_endpoint)[0][1:]))
            match = pattern.match(url)
            if match is not None:
                last, _, params = match
                el.params = params
                subpage_url = el
                url = f"/{params['url']}" if params.get('url', None) else url
                slug = url.split('/')[-1]
                break

        filter_data = {'slug': slug, 'polymorphic_ctype__in': subpage_url.page_types.all()} if subpage_url else {'slug': slug}

        instances = BasePage.active_on_site.filter(**filter_data).all()

        for instance in instances:
            if instance.absolute_url == url:
                instance = instance.get_real_instance()
                cache_service.set_instance_by_url(url, instance)
                if subpage_url:
                    instance.subpage_url = subpage_url
                return instance

        return None
