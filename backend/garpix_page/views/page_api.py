from rest_framework import status
from django.utils.translation import activate
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import django.apps
from django.conf import settings
from django.utils.module_loading import import_string


model_list = []
for model in django.apps.apps.get_models():
    try:
        if model.is_for_page_view():
            model_list.append(model)
    except:  # noqa
        pass


class PageApiView(views.APIView):

    @staticmethod
    def get_common_context(request=None, *args, **kwargs):
        if not hasattr(settings, 'COMMON_CONTEXT'):
            return {}
        context_function = import_string(settings.COMMON_CONTEXT)
        return context_function(request, *args, **kwargs)

    @staticmethod
    def get_instance_by_slug(slug, model_list):
        for m in model_list:
            instance = m.objects.filter(slug=slug).first()
            if instance:
                return instance
        return None

    def get_object(self, slug):
        obj = self.get_instance_by_slug(slug, model_list)
        if obj:
            return obj
        else:
            return None

    def get(self, request, slugs):
        language = "ru"
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            language = request.META['HTTP_ACCEPT_LANGUAGE']
        activate(language)

        slug_list = slugs.split('/')
        slug = slug_list.pop(-1)
        page = self.get_object(slug)

        if request.user.is_authenticated:
            user = get_user_model().objects.get(pk=request.user.pk)
        else:
            user = None

        common_context = self.get_common_context(request, obj=page, user=user)

        if page is None:
            data = {
                'type': None,
                'init_state': common_context
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        page_context = page.get_context(request, obj=page, user=user)
        common_context.update(page_context)

        data = {
            'type': None,
            'init_state': common_context,
        }
        return Response(data)
