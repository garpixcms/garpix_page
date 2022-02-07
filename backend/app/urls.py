from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.i18n import i18n_patterns
from multiurl import ContinueResolving, multiurl
from django.http import Http404
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from garpix_page.views.page import PageView
from garpix_page.views.page_api import PageApiView
from garpix_page.views.index import IndexView
from garpix_page.views.sitemap import sitemap_view
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'{}/page/(?P<slugs>.*)$'.format(settings.API_URL), PageApiView.as_view()),
    path('sitemap.xml', sitemap, sitemap_view(), name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)$', PageView.as_view(), name='page'),
        re_path(r'^(?P<url>.*?)/$', PageView.as_view(), name='page'),
        path('', IndexView.as_view()),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)
