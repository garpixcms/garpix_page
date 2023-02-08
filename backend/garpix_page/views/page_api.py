from rest_framework import status
from django.utils.translation import activate
from rest_framework import views
from rest_framework.response import Response
import django.apps
from django.utils.module_loading import import_string
from django.conf import settings

from garpix_page.mixins.views import PageViewMixin
from ..serializers.serializer import get_serializer
from ..utils.get_languages import get_languages

model_list = []
for model in django.apps.apps.get_models():
    try:
        if model.is_for_page_view():
            model_list.append(model)
    except:  # noqa
        pass


languages_list = get_languages()


class PageApiView(PageViewMixin, views.APIView):

    @staticmethod
    def get_error_page_response_data(page, request, page_name):
        return {
            'page_model': page_name,
            'init_state': {
                "object": None,
                "global": import_string(settings.GARPIX_PAGE_GLOBAL_CONTEXT)(request, page)
            }
        }

    def check_errors(self, page, request):
        if page is None:
            return Response(self.get_error_page_response_data(page, request, 'Page404'),
                            status=status.HTTP_404_NOT_FOUND)

        if getattr(page, 'login_required', False):
            if not request.user.is_authenticated:
                return Response(self.get_error_page_response_data(page, request, 'Page401'), status=status.HTTP_401_UNAUTHORIZED)

        if not page.has_permission_required(request):
            return Response(self.get_error_page_response_data(page, request, 'Page403'), status=status.HTTP_403_FORBIDDEN)

        if getattr(page, 'query_parameters_required', None) is not None:
            request_get = set(request.GET.keys())
            parameters = set(page.query_parameters_required)
            if request_get != parameters:
                return Response(self.get_error_page_response_data(page, request, 'Page404'), status=status.HTTP_404_NOT_FOUND)

        return None

    def get_object(self, slugs):

        obj = self.get_instance_by_slug(slugs, languages_list)
        return obj

    def get(self, request, slugs):  # noqa

        language = languages_list[0]
        if 'HTTP_ACCEPT_LANGUAGE' in request.META and request.META['HTTP_ACCEPT_LANGUAGE'] in languages_list:
            language = request.META['HTTP_ACCEPT_LANGUAGE']
        activate(language)

        page = self.get_object(slugs)

        errors = self.check_errors(page, request)
        if errors is not None:
            return errors

        page_context = page.get_context(request, object=page, user=request.user, api=True)
        for k, v in page_context.items():
            if hasattr(v, 'is_for_page_view'):
                model_serializer_class = get_serializer(v.__class__)
                page_context[k] = model_serializer_class(v, context={"request": request}).data
        if 'paginated_object_list' in page_context:
            try:
                serializer_class = get_serializer(page_context['paginated_object_list'][0].__class__)
                page_context['paginated_object_list'] = serializer_class(page_context['paginated_object_list'],
                                                                         context={"request": request}, many=True).data
            except Exception:
                page_context['paginated_object_list'] = list(
                    {'id': x.id, 'title': x.title, 'get_absolute_url': x.get_absolute_url()} for x in
                    page_context['paginated_object_list'])
        if 'paginator' in page_context:
            page_context['num_pages'] = page_context['paginator'].num_pages
            page_context['per_page'] = page_context['paginator'].per_page
            page_context.pop('paginator')

        page_context['global'] = import_string(settings.GARPIX_PAGE_GLOBAL_CONTEXT)(request, page)
        page_context['object'].update({
            'components': page.get_components_context(request, api=True)
        })
        data = {
            'page_model': page.get_model_class_name(),
            'init_state': page_context,
        }
        return Response(data)


class PageApiListView(views.APIView):
    def get(self, request):  # noqa
        from garpix_page.utils.get_garpix_page_models import get_garpix_page_models
        models_list = get_garpix_page_models()
        data = {}
        for model in models_list:
            for key, value in model.url_patterns().items():
                data.update({str(key).format(model_name=model.__name__): str(value['verbose_name']).format(model_title=model._meta.verbose_name)})
        return Response(data)
