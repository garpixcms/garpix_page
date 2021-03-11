import datetime
from django.utils.text import slugify


def get_file_path(instance, filename):
    """
    Формирует путь файла относительно года и месяца, чтобы множество файлов не скапливались на одном уровне.
    """
    import uuid
    ext = filename.split('.')[-1]
    fname = slugify(".".join(filename.split('.')[:-1]))
    if len(fname) < 3:
        fname += str(uuid.uuid4())
    today = datetime.date.today()
    filename = f'{fname}.{ext}'
    return f'uploads/{today.year}/{today.month}/{filename}'
