from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from multiurl import ContinueResolving, multiurl
from django.http import Http404
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from garpix_page.views.page import PageView
from garpix_page.views.page_api import PageApiView, PageApiListView
from garpix_page.views.index import IndexView
from garpix_page.views.robots import robots_txt
from garpix_page.views.sitemap import sitemap_view
from garpix_page.views.get_template import GetTemplate
from garpix_page.views.upload import DgjsUpload
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_template/', GetTemplate.as_view(), name='dgjs_get_template'),
    path('dgjs_upload/', DgjsUpload.as_view(), name='dgjs_upload'),
    path('page_lock/', include('garpix_admin_lock.urls')),
    re_path(r'{}/page_models_list/$'.format(settings.API_URL), PageApiListView.as_view()),
    re_path(r'{}/page/(?P<slugs>.*)/$'.format(settings.API_URL), PageApiView.as_view()),
    path('sitemap.xml', sitemap, sitemap_view(), name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)/$', PageView.as_view(), name='page'),
        path('', IndexView.as_view()),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)
