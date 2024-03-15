from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from garpix_page.views.index import IndexView
from garpix_page.views.page import PageView
from django.conf.urls.i18n import i18n_patterns
from multiurl.multiurl import ContinueResolving, multiurl
from django.http import Http404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/page_lock/', include('garpix_admin_lock.urls')),
    path('', include(('garpix_page.urls', 'garpix_page'), namespace='garpix_page')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    multiurl(
        path('', PageView.as_view()),
        re_path(r'^(?P<url>.*?)$', PageView.as_view(), name='page'),
        path('', IndexView.as_view()),
        catch=(Http404, ContinueResolving),
    ),
    prefix_default_language=settings.USE_DEFAULT_LANGUAGE_PREFIX,
)
