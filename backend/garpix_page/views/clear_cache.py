from django.contrib import messages
from django.http import HttpResponseRedirect
from garpix_page.cache import cache_service
from django.urls import reverse
from django.utils.translation import gettext as _


def clear_cache(request):
    cache_service.clear_all()
    link = request.META.get('HTTP_REFERER', reverse('admin:index'))
    messages.add_message(request, messages.INFO, _('Кэш очищен'))
    return HttpResponseRedirect(link)
