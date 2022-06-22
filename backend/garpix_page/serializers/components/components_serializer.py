from rest_polymorphic.serializers import PolymorphicSerializer

from ..serializer import get_serializer
from garpix_page.utils.get_garpix_page_models import get_garpix_page_component_models


def get_components_serializers_list():
    serializers_list = {}
    for model in get_garpix_page_component_models():
        serializers_list.update({model: get_serializer(model)})
    return serializers_list


class ComponentSerializer(PolymorphicSerializer):
    model_serializer_mapping = get_components_serializers_list()
