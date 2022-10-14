from django.contrib import messages
from django.http import HttpResponseRedirect
from garpix_page.cache import cache_service
from django.urls import reverse


def clear_cache(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))
    cache_service.clear_all()
    link = request.META.get('HTTP_REFERER', reverse('admin:index'))
    messages.add_message(request, messages.SUCCESS, 'Cache has been cleared', extra_tags='cache_cleared')
    return HttpResponseRedirect(link)
