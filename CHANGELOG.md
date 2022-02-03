### 2.13.0 (02.02.2022)

- Добавлены юнит-тесты, проверяющие страницы на корректные статусы. Используйте `python3 manage.py qa` для проверки.
- Добавлена возможность закрыть страницу правами. Переопределяйте `login_required` и `permission` модели `BasePage` (примеры в `README.md`).
- Глобальный контекст в api теперь возвращается при статусах 401, 403, 404.
- SEO теги в админке вынесены в отдельный таб.
- Исправлена ошибка при пагинации в структуре.

### 2.12.0 (26.09.2021)

- Исправлена ошибка с выбором языка при get_absolute_url при обращении по API.
- Изменен вывод переменных по пагинации для API.

### 2.11.0 (25.09.2021)

- Убраны внезапно выскакивающие разделы страниц. Оставлена только Структура страниц.
- Добавлен фильтр по типу страницы в Структуру страниц.
- Добавлено поле Тип в Структуру страниц при выводе списка.
- Добавлен фильтр по Сайтам в Структуру страниц.

### 2.10.0 (19.09.2021)

- Добавлен глобальный контекст для Page Api, задается так `GARPIX_PAGE_GLOBAL_CONTEXT = 'garpix_page.contexts.global_context.global_context'` и сама функция:
```python
def global_context(request, page):
    return {}
```

### 2.9.0 (14.09.2021)

- Использован `GarpixPaginator` из `garpix_utils` - позволяет выводить более красивую пагинацию. Изменен также шаблон для пагинации.

### 2.8.0 (10.09.2021)

- В кодогенерации сделана проверка на существующие строки в `__init__.py` файлах.
- Добавлен `breadcrumb.html`.
- При кодогенерации изменено содержимое шаблонов - подставляется согласно выбранному параметру `--base`.

### 2.7.0 (09.09.2021)

- Добавлен пакет `garpix_package`.
- Добавлена кодогенерация:
```bash
# Для обычных страниц
python3 backend/manage.py startpage --app=myapp --page=my --base=page

# Для списочных страниц
python3 backend/manage.py startpage --app=myapp --page=my_list --base=list

# Для поисковой страницы
python3 backend/manage.py startpage --app=myapp --page=search --base=search
```

### 2.6.0 (08.09.2021)

- Теперь нет ошибки при развертывании свежего проекта, т.к. добавлена индексная страница со ссылками 
на документацию (только если нет главной страницы).
- Исправлены ошибки после линтинга кода.
- По умолчанию, при создании страниц, выбраны все сайты (`Site.objects.all()`) в административной панели.
- Добавлена базовая модель `BaseListPage`, которую можно использовать для списочных страниц (т.е. у которых есть дочерние страницы).
- Добавлена вьюшка `sitemap_view` для карты сайта `/sitemap.xml`

### 2.5.0 (06.08.2021)

- Added method get_serializer() in BasePage. 

### 2.4.0 (03.08.2021)

- Set to page `title` BasePage `title`, if `seo_title` is not defined.

### 2.3.0 (03.08.2021)

- Added list_per_page to BasePageAdmin.

### 2.2.0 (23.06.2021)

- Added page_api urls for SPA sites.

### 2.1.0 (22.06.2021)

- Added admin-toolbar for staffs, use `{% include 'garpix_page/admin_toolbar.html' %}` in templates.

### 2.0.1 (22.06.2021)

- Fix bug with another home pages models.

### 2.0.0 (21.06.2021)

- Removed contexts and useless dicts from `settings.py`. All in models!

### 1.0.0 (11.03.2021)

- First release in pypi.org.
