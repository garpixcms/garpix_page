FILE_NAME_MODEL = '{app}/models/{page}_page.py'
FILE_NAME_MODEL_INIT = '{app}/models/__init__.py'

FILE_CONTENT_MODEL_BASE_PAGE = '''from django.db import models
from garpix_page.models import BasePage


class {page_capitalize}Page(BasePage):
    template = "pages/{page}.html"

    class Meta:
        verbose_name = "{page_capitalize}"
        verbose_name_plural = "{page_capitalize}s"
        ordering = ("-created_at",)
'''

FILE_CONTENT_MODEL_BASE_LIST_PAGE = '''from django.db import models
from garpix_page.models import BaseListPage


class {page_capitalize}Page(BaseListPage):
    paginate_by = 25
    template = 'pages/{page}.html'

    class Meta:
        verbose_name = "{page_capitalize}"
        verbose_name_plural = "{page_capitalize}s"
        ordering = ('-created_at',)
'''

FILE_CONTENT_MODEL_BASE_SEARCH_PAGE = '''from django.db import models
from garpix_page.models import BaseSearchPage


class {page_capitalize}Page(BaseSearchPage):
    paginate_by = 25
    template = 'pages/{page}.html'

    class Meta:
        verbose_name = "{page_capitalize}"
        verbose_name_plural = "{page_capitalize}s"
        ordering = ('-created_at',)
'''

FILE_CONTENT_MODEL_DICT = {
    'page': FILE_CONTENT_MODEL_BASE_PAGE,
    'list': FILE_CONTENT_MODEL_BASE_LIST_PAGE,
    'search': FILE_CONTENT_MODEL_BASE_SEARCH_PAGE,
}

FILE_CONTENT_MODEL_INIT = '''from .{page}_page import {page_capitalize}Page  # noqa
'''

FILE_NAME_TRANSLATION = '{app}/translation/{page}_page.py'
FILE_NAME_TRANSLATION_INIT = '{app}/translation/__init__.py'

FILE_CONTENT_TRANSLATION = '''from modeltranslation.translator import TranslationOptions, register
from ..models import {page_capitalize}Page


@register({page_capitalize}Page)
class {page_capitalize}PageTranslationOptions(TranslationOptions):
    pass
'''

FILE_CONTENT_TRANSLATION_INIT = '''from .{page}_page import {page_capitalize}PageTranslationOptions  # noqa
'''

FILE_NAME_ADMIN = '{app}/admin/{page}_page.py'
FILE_NAME_ADMIN_INIT = '{app}/admin/__init__.py'

FILE_CONTENT_ADMIN = '''from ..models.{page}_page import {page_capitalize}Page
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register({page_capitalize}Page)
class {page_capitalize}PageAdmin(BasePageAdmin):
    pass
'''

FILE_CONTENT_ADMIN_INIT = '''from .{page}_page import {page_capitalize}PageAdmin  # noqa
'''

FILE_NAME_TEMPLATE = '../frontend/templates/pages/{page}.html'

FILE_CONTENT_TEMPLATE_BASE_PAGE = '''{% extends 'base.html' %}

{% block content %}

{% include 'include/breadcrumb.html' %}

<h1>{{ object.title }}</h1>
{% endblock %}
'''

FILE_CONTENT_TEMPLATE_BASE_LIST_PAGE = '''{% extends 'base.html' %}

{% block content %}

{% include 'include/breadcrumb.html' %}

<h1>{{ object.title }}</h1>

{% for obj in paginated_object_list %}
    <div>
        <p><a href="{{ obj.get_absolute_url }}">{{ obj.title }}</a></p>
    </div>
{% empty %}
    <div>Записей пока нет.</div>
{% endfor %}

{% include 'include/pagination.html' %}

{% endblock %}
'''

FILE_CONTENT_TEMPLATE_BASE_SEARCH_PAGE = '''{% extends 'base.html' %}

{% block content %}

{% include 'include/breadcrumb.html' %}

<h1>{{ object.title }}</h1>

<form method="get">
  <div class="form-row align-items-center">
    <div class="col-auto">
      <label class="sr-only" for="q">Поиск</label>
      <input type="text" class="form-control mb-2" name="q" id="q" value="{{ q }}" placeholder="Введите поисковый запрос...">
    </div>
    <div class="col-auto">
      <button type="submit" class="btn btn-primary mb-2">Найти</button>
    </div>
  </div>
</form>

{% for obj in paginated_object_list %}
    <div>
        <p><a href="{{ obj.get_absolute_url }}">{{ obj.title }}</a></p>
    </div>
{% empty %}
    <div>Ничего не найдено.</div>
{% endfor %}

{% include 'include/pagination.html' %}

{% endblock %}
'''

FILE_CONTENT_TEMPLATE_DICT = {
    'page': FILE_CONTENT_TEMPLATE_BASE_PAGE,
    'list': FILE_CONTENT_TEMPLATE_BASE_LIST_PAGE,
    'search': FILE_CONTENT_TEMPLATE_BASE_SEARCH_PAGE,
}

FILE_NAME_APP_INIT = '{app}/__init__.py'
FILE_CONTENT_APP_INIT = '''default_app_config = '{app}.apps.{app_capitalize}Config'
'''

FILE_NAME_APPS = '{app}/apps.py'
FILE_CONTENT_APPS = '''from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class {app_capitalize}Config(AppConfig):
    name = '{app}'
    verbose_name = _('{app_capitalize}')
'''

FILE_NAME_MIGRATIONS_INIT = '{app}/migrations/__init__.py'
