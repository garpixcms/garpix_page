from garpix_page.models import GarpixPageSiteConfiguration


from django.contrib.sitemaps import GenericSitemap
from garpix_page.models.base_page import BasePage


def sitemap_view():
    pages = {
        'queryset': BasePage.on_site.filter(is_active=True, display_on_sitemap=True).order_by('title'),
        'date_field': 'created_at'
    }
    extra_data = {
        'priority': 1.0
    }
    try:
        config = GarpixPageSiteConfiguration.get_solo()
        extra_data.update({
            'changefreq': config.sitemap_frequency
        })
    except Exception:
        pass

    return {
        'sitemaps': {
            'pages': GenericSitemap(
                pages,
                **extra_data
            ),
        }
    }
