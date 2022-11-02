from django.conf import settings
from django.utils.module_loading import import_string

from garpix_page.cache import cache_service
from garpix_page.utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix

celery_app = import_string(settings.GARPIXCMS_CELERY_SETTINGS)


@celery_app.task()
def clear_child_cache(instance_pk):
    from garpix_page.models import BasePage

    instance = BasePage.objects.get(pk=instance_pk)

    pages = BasePage.objects.get_queryset_descendants(instance.get_children(), include_self=True)

    for page in pages:
        cache_service.reset_url_info_by_page(page, get_current_language_code_url_prefix())
