from .get_languages import get_languages


def get_exclude_fields(model):
    langs = get_languages()
    exclude_fields = []
    model_fields = [field.name for field in model._meta.get_fields()]

    for field in model_fields:
        for lang in langs:
            if f'{field}_{lang.replace("-", "_")}' not in model_fields:
                break
        else:
            for lang in langs:
                exclude_fields.append(f'{field}_{lang.replace("-", "_")}')
    return exclude_fields
