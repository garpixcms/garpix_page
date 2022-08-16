from rest_framework.serializers import ModelSerializer


def get_serializer(model):
    if model.get_serializer(model) is not None:
        return model.get_serializer(model)
    return type(f'{model.__name__}Serializer', (ModelSerializer, ), {
        'Meta': type('Meta', (object,), {
            'model': model,
            'exclude': ('sites', 'lft', 'rght', 'tree_id', 'level', 'polymorphic_ctype', 'parent',)
            # 'fields': '__all__'
        })
    })


def get_components_serializer(model):
    if model.get_serializer(model) is not None:
        return model.get_serializer(model)

    return type(f'{model.__name__}Serializer', (ModelSerializer, ), {
        'Meta': type('Meta', (object,), {
            'model': model,
            'exclude': ('polymorphic_ctype', 'pages')
        })
    })
