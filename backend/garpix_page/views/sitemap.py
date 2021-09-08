from django.contrib.sitemaps import GenericSitemap
from ..models.base_page import BasePage


def sitemap_view():
    return {
        'sitemaps': {
            'pages': GenericSitemap(
                {
                    'queryset': BasePage.objects.filter(is_active=True).order_by('title'),
                    'date_field': 'created_at'
                },
                priority=1.0
            ),
        }
    }
