from rest_framework.serializers import ModelSerializer


def get_serializer(model):
    if model.serializer is not None:
        return model.serializer
    return type(f'{model.__name__}Serializer', (ModelSerializer, ), {
        'Meta': type('Meta', (object,), {
            'model': model,
            'fields': '__all__'
        })
    })
