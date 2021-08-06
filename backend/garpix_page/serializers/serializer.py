from rest_framework.serializers import ModelSerializer


def get_serializer(model):
    if model.get_serializer(model) is not None:
        return model.get_serializer(model)
    return type(f'{model.__name__}Serializer', (ModelSerializer, ), {
        'Meta': type('Meta', (object,), {
            'model': model,
            'fields': '__all__'
        })
    })
