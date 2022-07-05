from rest_framework.serializers import ModelSerializer
from rest_polymorphic.serializers import PolymorphicSerializer

from ..serializer import get_serializer
from garpix_page.utils.get_garpix_page_models import get_garpix_page_component_models


def get_components_serializers_list():
    serializers_list = {}
    for model in get_garpix_page_component_models():
        serializers_list.update({model: get_serializer(model)})
    return serializers_list


def get_components_serializer(model):
    if model.get_serializer(model) is not None:
        return model.get_serializer(model)
    return type(f'{model.name}Serializer', (ModelSerializer, ), {
        'Meta': type('Meta', (object,), {
            'model': model,
            'exclude': ('polymorphic_ctype', 'pages')
        })
    })


class ComponentSerializer(PolymorphicSerializer):
    model_serializer_mapping = get_components_serializers_list()
