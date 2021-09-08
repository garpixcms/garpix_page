(31.08.2021)

- Added abstract model CustomBasePage
- Added to utilities FIELD_BASE_PAGE 

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
