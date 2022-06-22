from django.utils import translation
from django.conf import settings


def get_current_language_code_url_prefix():
    current_language_code_url_prefix = translation.get_language()
    try:
        use_default_prefix = settings.USE_DEFAULT_LANGUAGE_PREFIX
    except:  # noqa
        use_default_prefix = True
    if not use_default_prefix and current_language_code_url_prefix == settings.LANGUAGE_CODE:
        current_language_code_url_prefix = ''
    elif current_language_code_url_prefix is None:
        current_language_code_url_prefix = ''
    else:
        current_language_code_url_prefix = '/' + current_language_code_url_prefix
    return current_language_code_url_prefix
