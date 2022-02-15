from django.conf import settings
from django.http import Http404

from ..utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix
from ..utils.get_garpix_page_models import get_garpix_page_models
from ..utils.check_redirect import check_redirect
from django.shortcuts import redirect
from django.views.generic import DetailView


class PageView(DetailView):
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

    def _get_object_list_by_url(self, url):
        obj_list = []
        slugs = url.rstrip('/').split('/')
        slug = slugs[-1]
        parent_slug = slugs[-2] if len(slugs) > 2 else None
        for model in get_garpix_page_models():
            if parent_slug:
                _obj = model.on_site.filter(slug=slug, parent__slug=parent_slug).first()
            else:
                _obj = model.on_site.filter(slug=slug).first()
            if _obj:
                obj_list.append(_obj)
        return obj_list

    def get_object(self, queryset=None):
        """
        Метод для получения объекта страницы.
        Сравнивает текущий урл со slug, которые мы получаем из родительских страниц нашей страницы.
        """
        current_language_code_url_prefix = get_current_language_code_url_prefix()
        url = self.kwargs.get('url', None)
        # home pages
        if url is None or url == '':
            return self._get_home_page()
        # get page object
        obj_list = self._get_object_list_by_url(url)
        obj = None
        for item in obj_list:
            if item.get_absolute_url() == f'{current_language_code_url_prefix}/{url}':
                obj = item
                break
        if not obj:
            raise Http404
        if not obj.is_active:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
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
