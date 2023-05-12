from garpix_page.models import GarpixPageSiteConfiguration
from django.contrib.sitemaps import GenericSitemap
from garpix_page.models.base_page import BasePage
from django.contrib.sitemaps.views import sitemap


def sitemap_view(request, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

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

    sitemaps = {
            'pages': GenericSitemap(
                pages,
                **extra_data
            ),
    }
    return sitemap(request, sitemaps, section, template_name, content_type)
