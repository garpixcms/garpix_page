import os
from django.conf import settings
from .constants import *


def snake_to_camel_case(text_snake):
    return '{}'.format(
        text_snake.title().replace('_', ''),
    )


def create_file(directory, file_name, file_content):
    path = os.path.join(directory, file_name)
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.write(file_content)


def create_or_append_file(directory, file_name, file_content):
    path = os.path.join(directory, file_name)
    if not os.path.isfile(path):
        create_file(directory, file_name, file_content)
    else:
        with open(path, 'r') as f:
            lines = f.readlines()
            if file_content in lines:
                return
        with open(path, 'a') as f:
            f.write(file_content)


def generate_page(app, page, base):
    base_directory = os.path.abspath(os.path.join(settings.BASE_DIR))
    available_bases = ['page', 'list', 'search']
    if base not in available_bases:
        raise Exception(f'Неправильно выбран параметр base. Допустимые значения: {", ".join(available_bases)}')
    # create models
    directory = os.path.join(base_directory, os.path.dirname(FILE_NAME_MODEL.format(app=app, page=page)))
    os.makedirs(
        directory,
        exist_ok=True
    )
    # models page
    base_name = os.path.basename(FILE_NAME_MODEL.format(app=app, page=page))
    content = FILE_CONTENT_MODEL_DICT[base].format(app=app, page=page, page_capitalize=snake_to_camel_case(page))
    create_file(directory, base_name, content)
    # models init
    base_name = os.path.basename(FILE_NAME_MODEL_INIT.format(app=app, page=page))
    content = FILE_CONTENT_MODEL_INIT.format(page=page, page_capitalize=snake_to_camel_case(page))
    create_or_append_file(directory, base_name, content)

    print(f'Не забудьте поменять verbose_name и verbose_name_plural в файлах: backend/{FILE_NAME_MODEL.format(app=app, page=page)}')

    # create admin
    directory = os.path.join(base_directory, os.path.dirname(FILE_NAME_ADMIN.format(app=app, page=page)))
    os.makedirs(
        directory,
        exist_ok=True
    )
    # admin page
    base_name = os.path.basename(FILE_NAME_ADMIN.format(app=app, page=page))
    content = FILE_CONTENT_ADMIN.format(app=app, page=page, page_capitalize=snake_to_camel_case(page))
    create_file(directory, base_name, content)
    # admin init
    base_name = os.path.basename(FILE_NAME_ADMIN_INIT.format(app=app, page=page))
    content = FILE_CONTENT_ADMIN_INIT.format(page=page, page_capitalize=snake_to_camel_case(page))
    create_or_append_file(directory, base_name, content)

    # create translation
    directory = os.path.join(base_directory, os.path.dirname(FILE_NAME_TRANSLATION.format(app=app, page=page)))
    os.makedirs(
        directory,
        exist_ok=True
    )
    # translation page
    base_name = os.path.basename(FILE_NAME_TRANSLATION.format(app=app, page=page))
    content = FILE_CONTENT_TRANSLATION.format(app=app, page=page, page_capitalize=snake_to_camel_case(page))
    create_file(directory, base_name, content)
    # translation init
    base_name = os.path.basename(FILE_NAME_TRANSLATION_INIT.format(app=app, page=page))
    content = FILE_CONTENT_TRANSLATION_INIT.format(page=page, page_capitalize=snake_to_camel_case(page))
    create_or_append_file(directory, base_name, content)

    # create template
    directory = os.path.join(base_directory, os.path.dirname(FILE_NAME_TEMPLATE.format(page=page)))
    os.makedirs(
        directory,
        exist_ok=True
    )
    # template page
    base_name = os.path.basename(FILE_NAME_TEMPLATE.format(page=page))
    content = FILE_CONTENT_TEMPLATE_DICT[base]
    create_file(directory, base_name, content)

    # create app init
    directory = os.path.join(base_directory, os.path.dirname(FILE_NAME_APP_INIT.format(app=app)))
    os.makedirs(
        directory,
        exist_ok=True
    )
    # app init
    base_name = os.path.basename(FILE_NAME_APP_INIT.format(app=app))
    content = FILE_CONTENT_APP_INIT.format(app=app, app_capitalize=snake_to_camel_case(app))
    create_file(directory, base_name, content)

    # create app apps
    directory = os.path.join(base_directory, os.path.dirname(FILE_NAME_APPS.format(app=app)))
    os.makedirs(
        directory,
        exist_ok=True
    )
    # app apps
    base_name = os.path.basename(FILE_NAME_APPS.format(app=app))
    content = FILE_CONTENT_APPS.format(app=app, app_capitalize=snake_to_camel_case(app))
    create_file(directory, base_name, content)

    print(f'Не забудьте проверить, что verbose_name указан верно в файле: backend/{FILE_NAME_APPS.format(app=app)}')

    # create migrations
    directory = os.path.join(base_directory, os.path.dirname(FILE_NAME_MIGRATIONS_INIT.format(app=app)))
    os.makedirs(
        directory,
        exist_ok=True
    )
    # app apps
    base_name = os.path.basename(FILE_NAME_MIGRATIONS_INIT.format(app=app))
    create_file(directory, base_name, '')
