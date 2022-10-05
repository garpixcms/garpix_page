from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from garpix_page.utils.get_exclude_fields import get_exclude_fields


def get_serializer(model):
    if model.get_serializer(model) is not None:
        return model.get_serializer(model)

    return type(f'{model.__name__}Serializer', (ModelSerializer, ), {
        'seo_title': ReadOnlyField(source='get_seo_title'),
        'seo_keywords': ReadOnlyField(source='get_seo_keywords'),
        'seo_description': ReadOnlyField(source='get_seo_description'),
        'seo_author': ReadOnlyField(source='get_seo_author'),
        'seo_og_type': ReadOnlyField(source='get_seo_og_type'),
        'Meta': type('Meta', (object,), {
            'model': model,
            'exclude': ('sites', 'lft', 'rght', 'tree_id', 'level', 'polymorphic_ctype', 'parent',) + tuple(get_exclude_fields(model))
            # 'fields': '__all__'
        })
    })


def get_components_serializer(model):
    if model.get_serializer(model) is not None:
        return model.get_serializer(model)

    return type(f'{model.__name__}Serializer', (ModelSerializer, ), {
        'Meta': type('Meta', (object,), {
            'model': model,
            'exclude': ('polymorphic_ctype', 'pages') + tuple(get_exclude_fields(model))
        })
    })
