from garpix_page.cache import cache_service
from garpix_page.models import BasePage, HookPage
from garpix_page.utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix
from django.utils.translation import activate
from django.urls.resolvers import RoutePattern


class PageViewMixin:

    @staticmethod
    def get_absolute_url_from_request(slug_list, slug):
        current_language_code_url_prefix = get_current_language_code_url_prefix()
        if slug != '':
            return "{}/{}".format(current_language_code_url_prefix, '/'.join(slug_list))
        return "{}".format(current_language_code_url_prefix) if len(current_language_code_url_prefix) > 1 else '/'

    @classmethod
    def get_instance_by_slug(cls, slugs, languages_list):
        hook_pages = HookPage.on_site.all()

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

        # if instance_cache is not None:
        #     return instance_cache

        for el in hook_pages:
            pattern = RoutePattern(el.get_pattern())
            match = pattern.match(url)
            if match is not None:
                last, _, params = match
                el.params = params
                return el

        instances = BasePage.on_site.filter(slug=slug, is_active=True).all()

        for instance in instances:
            if instance.absolute_url == url:
                instance = instance.get_real_instance()
                cache_service.set_instance_by_url(url, instance)
                return instance

        return None
