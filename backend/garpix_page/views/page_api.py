from rest_framework import status
from django.utils.translation import activate
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import django.apps
from django.conf import settings
from django.utils.module_loading import import_string
from ..models.base_page import BasePage
from ..serializers.serializer import get_serializer


model_list = []
for model in django.apps.apps.get_models():
    try:
        if model.is_for_page_view():
            model_list.append(model)
    except:  # noqa
        pass


class PageApiView(views.APIView):

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

        if page is None:
            data = {
                'page_model': None,
                'init_state': {}
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        page_context = page.get_context(request, object=page, user=user)
        page_context.pop('request')
        for k, v in page_context.items():
            if hasattr(v, 'is_for_page_view'):
                model_serializer_class = get_serializer(v.__class__)
                page_context[k] = model_serializer_class(v).data
        data = {
            'page_model': page.__class__.__name__,
            'init_state': page_context,
        }
        return Response(data)
