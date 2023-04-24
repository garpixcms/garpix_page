import re

from django.urls.resolvers import RoutePattern, _route_to_regex

from django.utils.translation import activate

from garpix_page.utils.get_garpix_page_models import get_garpix_page_models


class PageViewMixin:

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

        url = f"/{'/'.join(slug_list)}"

        page_models = get_garpix_page_models()
        active_models = []
        for el in page_models:
            for key, value in el.url_patterns().items():
                pattern = RoutePattern(r'(<url>){}'.format(value['pattern']))
                pattern.regex = re.compile('^/(?P<url>.*){}$'.format(_route_to_regex(value['pattern'], pattern._is_endpoint)[0][1:]))
                match = pattern.match(url)
                if match is not None:
                    last, _, params = match

                    el_url = f"/{params.pop('url')}"

                    active_models.append({
                        'model': el,
                        'params': params,
                        'pattern': key,
                        'url': el_url,
                        'permissions': value.get('permissions', el.permissions)
                    })

        for model in active_models:
            instance = model['model'].active_on_site.filter(url=model['url']).first()

            if instance:
                instance.subpage_params = model['params']
                instance.subpage_key = model['pattern']
                instance.permissions = model['permissions']
                return instance

        return None
