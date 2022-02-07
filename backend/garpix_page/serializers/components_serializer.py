from collections import defaultdict

from rest_framework.serializers import Serializer
from rest_polymorphic.serializers import PolymorphicSerializer

from .serializer import get_serializer
from garpix_page.utils.get_garpix_page_models import get_garpix_page_component_models


def get_components_serializers_list():
    serializers_list = {}
    for model in get_garpix_page_component_models():
        serializers_list.update({model: get_serializer(model)})
    return serializers_list


class ComponentSerializer(PolymorphicSerializer):
    model_serializer_mapping = get_components_serializers_list()


def get_components_tree(components_list, request):
    components = ComponentSerializer(components_list, many=True, context={"request": request}).data

    components_response = []
    current_path = []
    for component in components:
        component.update({"children": []})
        if component["level"] == 0:
            components_response.append(component)
            current_path = [components_response[-1]]
        else:
            level = component["level"] - current_path[-1]["level"]
            if level <= 0:
                current_path.pop(-level)
            current_path[(level-1)]["children"].append(component)
            current_path.append(component)
    return components_response
