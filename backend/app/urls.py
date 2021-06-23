from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.i18n import i18n_patterns
from garpix_page.views.page import PageView
from garpix_page.views.page_api import PageApiView
from multiurl import ContinueResolving, multiurl
from django.http import Http404
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'page_api/(?P<slugs>.*)$', PageApiView.as_view()),
]

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)$', PageView.as_view(), name='page'),
        re_path(r'^(?P<url>.*?)/$', PageView.as_view(), name='page'),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)
