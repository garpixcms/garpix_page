from django.conf import settings
from django.http import Http404

from garpix_page.mixins.views import PageViewMixin
from ..utils.get_garpix_page_models import get_garpix_page_models
from ..utils.check_redirect import check_redirect
from django.shortcuts import redirect
from django.views.generic import DetailView

from ..utils.get_languages import get_languages
from urllib.parse import urlencode

languages_list = get_languages()


class PageView(PageViewMixin, DetailView):
    def get_template_names(self):
        """
        Метод для получения темплейта для страницы.
        Структуру темплейтов можно посмотреть в модели page.models.Page.
        """
        if self.object is not None:
            return [self.object.get_template()]
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object is not None:
            context.update(self.object.get_context(self.request, object=self.object))
        return context

    def _get_home_page(self):
        for Model in get_garpix_page_models():
            home_page = Model.on_site.filter(slug='', is_active=True).first()
            if home_page is not None:
                return home_page
        raise Http404

    def get_object(self, queryset=None):
        """
        Метод для получения объекта страницы.
        Сравнивает текущий урл со slug, которые мы получаем из родительских страниц нашей страницы.
        """
        url = self.kwargs.get('url', None)
        # home pages
        if url is None or url == '':
            return self._get_home_page()

        obj = self.get_instance_by_slug(url, languages_list)

        return obj

    def _check_permissions(self, request):

        user = request.user

        if getattr(self.object, 'login_required', False):
            if not user.is_authenticated:
                return False
        if not self.object.has_permission_required(request):
            return False

        if getattr(self.object, 'query_parameters_required', None) is not None:
            request_get = set(request.GET.keys())
            parameters = set(self.object.query_parameters_required)
            if request_get != parameters:
                return False
        return True

    def get(self, request, *args, **kwargs):
        from django.shortcuts import render

        url = self.kwargs.get('url', None)

        if url and url[-1] == '/':
            parameters = f'?{urlencode(request.GET)}' if urlencode(request.GET) else ''
            return redirect(f"/{url.rstrip('/')}{parameters}")

        self.object = self.get_object()

        if not self.object:
            try:
                response = render(request, "404.html", context={})
                response.status_code = 404
                return response
            except Exception:
                raise Http404

        if not self._check_permissions(request):
            return redirect(settings.LOGIN_URL)

        context = self.get_context_data(object=self.object)
        redir = check_redirect(request, context)
        if redir:
            return redirect(redir)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        if getattr(self.object, 'login_required', False):
            if not user.is_authenticated:
                return redirect(settings.LOGIN_URL)
        if not self.object.has_permission_required(request):
            return redirect(settings.LOGIN_URL)
        context = self.get_context_data(object=self.object)
        redir = check_redirect(request, context)
        if redir:
            return redirect(redir)
        return self.render_to_response(context)
