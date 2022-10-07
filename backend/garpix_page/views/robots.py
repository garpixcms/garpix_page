from django.http import HttpResponse
from django.views.decorators.http import require_GET

from garpix_page.models import GarpixPageSiteConfiguration


@require_GET
def robots_txt(request):

    try:
        lines = GarpixPageSiteConfiguration.get_solo().robots_txt
    except Exception:
        lines = ''
    return HttpResponse(lines, content_type="text/plain")
