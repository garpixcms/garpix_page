from django.conf import settings
from django.utils.module_loading import import_string

from garpix_page.cache import cache_service
from garpix_page.utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix

celery_app = import_string(settings.GARPIXCMS_CELERY_SETTINGS)


@celery_app.task()
def clear_child_cache(children_ids):
    from garpix_page.models import BasePage
    pages = BasePage.objects.filter(id__in=children_ids)
    for page in pages:
        cache_service.clear_all_by_page(page, get_current_language_code_url_prefix())
