from django.urls import path, re_path
from django.conf import settings
from garpix_page.views.page_api import PageApiView, PageApiListView
from garpix_page.views.robots import robots_txt
from garpix_page.views.sitemap import sitemap_view

app_name = 'garpix_page'

urlpatterns = [
    re_path(r'{}/page_models_list/$'.format(settings.API_URL), PageApiListView.as_view()),
    re_path(r'{}/page/(?P<slugs>.*)/$'.format(settings.API_URL), PageApiView.as_view()),
    re_path(r'{}/page/(?P<slugs>.*)$'.format(settings.API_URL), PageApiView.as_view()),
    path('sitemap.xml', sitemap_view, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]
