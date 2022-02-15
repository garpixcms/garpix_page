from rest_framework import status
from django.utils.translation import activate
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import django.apps
from django.utils.module_loading import import_string
from django.conf import settings
from ..serializers.serializer import get_serializer

from ..utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix

model_list = []
for model in django.apps.apps.get_models():
    try:
        if model.is_for_page_view():
            model_list.append(model)
    except:  # noqa
        pass

languages_list = [x[0] for x in settings.LANGUAGES]


class PageApiView(views.APIView):

    @staticmethod
    def get_absolute_url_from_request(slug_list, slug):
        current_language_code_url_prefix = get_current_language_code_url_prefix()
        if slug != '':
            return "{}/{}".format(current_language_code_url_prefix, '/'.join(slug_list))
        return "{}".format(current_language_code_url_prefix) if len(current_language_code_url_prefix) > 1 else '/'

    @staticmethod
    def get_instance_by_slug(slug):
        for m in model_list:
            instance = m.objects.filter(slug=slug).first()
            if instance:
                return instance
        return None

    def get_object(self, slug):
        obj = self.get_instance_by_slug(slug)
        return obj

    @staticmethod
    def get_error_page_response_data(page, request):
        return {
            'page_model': page.__class__.__name__ if page is not None else None,
            'init_state': {
                "object": None,
                "global": import_string(settings.GARPIX_PAGE_GLOBAL_CONTEXT)(request, page)
            }
        }

    def check_errors(self, page, request):
        if page is None:
            return Response(self.get_error_page_response_data(page, request), status=status.HTTP_404_NOT_FOUND)

        if getattr(page, 'login_required', False):
            if not request.user.is_authenticated:
                return Response(self.get_error_page_response_data(page, request), status=status.HTTP_401_UNAUTHORIZED)

        if not page.has_permission_required(request):
            return Response(self.get_error_page_response_data(page, request), status=status.HTTP_403_FORBIDDEN)

        return None

    def get(self, request, slugs):

        language = languages_list[0]
        if 'HTTP_ACCEPT_LANGUAGE' in request.META and request.META['HTTP_ACCEPT_LANGUAGE'] in languages_list:
            language = request.META['HTTP_ACCEPT_LANGUAGE']
        activate(language)

        slug_list = slugs.split('/')

        if slug_list[0] in languages_list:
            activate(slug_list[0])
            slug_list.pop(0)

        if len(slug_list) == 0:
            slug_list.append('')

        if len(slug_list) > 1 and slug_list[-1] == '':
            slug_list.pop(-1)

        slug = slug_list[-1]
        page = self.get_object(slug)

        if page and page.absolute_url != self.get_absolute_url_from_request(slug_list, slug):
            page = None

        errors = self.check_errors(page, request)
        if errors is not None:
            return errors

        if request.user.is_authenticated:
            user = get_user_model().objects.get(pk=request.user.pk)
        else:
            user = None

        page_context = page.get_context(request, object=page, user=user)
        page_context.pop('request')
        for k, v in page_context.items():
            if hasattr(v, 'is_for_page_view'):
                model_serializer_class = get_serializer(v.__class__)
                page_context[k] = model_serializer_class(v).data
        if 'paginated_object_list' in page_context:
            page_context['paginated_object_list'] = list(
                {'id': x.id, 'title': x.title, 'get_absolute_url': x.get_absolute_url()} for x in
                page_context['paginated_object_list'])
        if 'paginator' in page_context:
            page_context['num_pages'] = page_context['paginator'].num_pages
            page_context['per_page'] = page_context['paginator'].per_page
            page_context.pop('paginator')

        page_context['global'] = import_string(settings.GARPIX_PAGE_GLOBAL_CONTEXT)(request, page)
        data = {
            'page_model': page.__class__.__name__,
            'init_state': page_context,
        }
        return Response(data)
