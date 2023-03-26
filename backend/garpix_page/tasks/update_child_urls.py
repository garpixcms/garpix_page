from django.conf import settings
from django.utils.module_loading import import_string

from garpix_page.utils.set_children_urls import set_children_url

celery_app = import_string(settings.GARPIXCMS_CELERY_SETTINGS)


@celery_app.task()
def clear_child_cache(id):
    from garpix_page.models import BasePage

    instance = BasePage.objects.get(pk=id)
    children = instance.get_children()

    pages_to_update = []
    set_children_url(instance, children, pages_to_update)

    BasePage.objects.bulk_update(pages_to_update, ['url'])
    BasePage.objects.rebuild()
