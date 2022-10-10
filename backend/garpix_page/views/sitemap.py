from garpix_page.models import GarpixPageSiteConfiguration


from django.contrib.sitemaps import GenericSitemap
from garpix_page.models.base_page import BasePage


def sitemap_view():
    pages = {
        'queryset': BasePage.on_site.filter(is_active=True).order_by('title'),
        'date_field': 'created_at'
    }

    try:
        config = GarpixPageSiteConfiguration.get_solo().robots_txt
        pages.update({
            'changefreq': config.sitemap_frequency
        })
    except Exception:
        pass
    return {
        'sitemaps': {
            'pages': GenericSitemap(
                pages,
                priority=1.0
            ),
        }
    }
