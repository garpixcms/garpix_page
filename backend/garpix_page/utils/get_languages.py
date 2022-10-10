from django.conf import settings


def get_languages():
    return [x[0] for x in settings.LANGUAGES]
