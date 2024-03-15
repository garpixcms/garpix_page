from django.conf import settings
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils import translation
from django.utils.functional import cached_property
from django.db import models
from django.urls import reverse
from django.contrib.sites.models import Site
from rest_framework.views import APIView
from garpix_page.utils.all_sites import get_all_sites
from garpix_page.utils.get_file_path import get_file_path
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey, PolymorphicMPTTModelManager
from django.utils.html import format_html
from garpix_utils.managers import GCurrentSiteManager, GPolymorphicCurrentSiteManager, ActiveOnSiteManager
from ..cache import cache_service
from ..mixins import CloneMixin
from garpix_admin_lock.mixins import PageLockViewMixin

from ..tasks import clear_child_cache
from ..utils.get_current_language_code_url_prefix import get_current_language_code_url_prefix
from ..utils.set_children_urls import set_children_url


class BasePage(CloneMixin, PolymorphicMPTTModel, PageLockViewMixin):
    """
    Базовая страница, на основе которой создаются все прочие страницы.
    """
    title = models.CharField(max_length=255, verbose_name='Название')
    is_active = models.BooleanField(default=True, verbose_name='Включено')
    display_on_sitemap = models.BooleanField(default=True, verbose_name='Отображать в карте сайта')
    slug = models.SlugField(max_length=150, verbose_name='ЧПУ', blank=True, default='')
    sites = models.ManyToManyField(Site, default=get_all_sites, verbose_name='Сайты для отображения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    seo_title = models.CharField(max_length=250, verbose_name='SEO заголовок страницы (title)', blank=True, default='')
    seo_keywords = models.CharField(max_length=250, verbose_name='SEO ключевые слова (keywords)', blank=True,
                                    default='')
    seo_description = models.TextField(verbose_name='SEO описание (description)', blank=True, default='')
    seo_author = models.CharField(max_length=250, verbose_name='SEO автор (author)', blank=True, default='')
    seo_og_type = models.CharField(max_length=250, verbose_name='SEO og:type', blank=True, default="website")
    seo_image = models.FileField(upload_to=get_file_path, blank=True, null=True, verbose_name='SEO изображение')
    parent = PolymorphicTreeForeignKey('self', null=True, blank=True, related_name='children',
                                       db_index=True, verbose_name='Родительская страница', on_delete=models.SET_NULL,
                                       limit_choices_to={})
    url = models.CharField(max_length=255, default='', blank=True, verbose_name='Полный URL страницы')

    # objects = models.Manager()
    objects = PolymorphicMPTTModelManager()
    on_site = GCurrentSiteManager()
    polymorphic_on_site = GPolymorphicCurrentSiteManager()
    active_on_site = ActiveOnSiteManager()

    template = 'garpix_page/default.html'
    searchable_fields = ('title',)
    serializer = None  # default is generator of serializers: garpix_page.serializers.serializer.get_serializer
    permissions = None
    subpage_params = None
    subpage_key = None

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = 'Структура страниц | Pages structure'
        verbose_name_plural = 'Структура страниц | Pages structure'
        ordering = ('created_at', 'title',)

    def get_model_class_name(self):
        if self.subpage_key:
            return str(self.subpage_key).format(model_name=self.__class__.__name__)
        return self.__class__.__name__

    def __str__(self):
        return self.title

    @cached_property
    def _default_site(self):
        return Site.objects.get(pk=getattr(settings, 'SITE_ID', 1))

    _default_site.short_description = 'Default Site'

    def get_seo_template_keys(self):
        return self.__dict__

    @classmethod
    def seo_template_keys_list(cls):
        return [(f.name, f.verbose_name) for f in cls._meta.fields if hasattr(f, 'verbose_name') and (
                isinstance(f, models.CharField) or isinstance(f, models.TextField))]

    def get_verbose_model_name(self):
        return self._meta.verbose_name

    get_verbose_model_name.short_description = 'Название модели'

    def get_absolute_url(self):
        return self.absolute_url

    get_absolute_url.short_description = 'URL'

    def get_absolute_url_html(self):
        return f'<a href="{self.absolute_url}" target="_blank">{self.absolute_url}</a>'

    get_absolute_url_html.short_description = 'URL'
    get_absolute_url_html.allow_tags = True

    @cached_property
    def absolute_url(self):
        current_language_code_url_prefix = get_current_language_code_url_prefix()
        return "{}{}".format(current_language_code_url_prefix,
                             self.url) if current_language_code_url_prefix else self.url

    absolute_url.short_description = 'URL'

    def set_url(self, parent=None):

        parent = parent or self.parent

        self.url = ''

        if parent and parent.url != '/':
            self.url = parent.url

        self.url += f"/{self.slug}"

    @cached_property
    def get_sites(self):
        res = 'n/a'
        if self.sites.all().count() > 0:
            res = ''
            for site in self.sites.all():
                res += f'{site.domain} '
        return res

    get_sites.short_description = 'Sites'

    def get_template(self):
        return self.template

    def get_context(self, request=None, *args, **kwargs):

        return {
            'object': self,
            'subpages': self.get_subpages_list(),
            'components': self.get_components_context(request, api=kwargs.get('api', False))
        }

    @classmethod
    def is_for_page_view(cls):
        return True

    def get_breadcrumbs(self):
        result = []
        obj = self
        result.append(obj)
        while obj.parent is not None:
            result.insert(0, obj.parent)
            obj = obj.parent
        return result

    def get_admin_url_edit_object(self):
        url = reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=[self.id])
        return url

    def get_serializer(self):
        return self.serializer

    def model_name(self):
        real_instance = self.get_real_instance_class()
        if real_instance:
            return real_instance._meta.verbose_name  # noqa
        return '- нет -'

    model_name.short_description = 'Тип'

    def has_permission_required(self, request):

        view = APIView()
        view.queryset = type(self).objects.filter(id=self.id)
        if self.permissions is not None:
            for permission in [permission() for permission in self.permissions]:
                if not permission.has_object_permission(request, view, self) or not permission.has_permission(request,
                                                                                                              view):
                    return False
        return True

    def get_components_context(self, request, api=False):
        context = []
        components = self.pagecomponent_set.filter(component__is_active=True, component__is_deleted=False).order_by(
            'view_order')
        for component in components:
            component_context = {
                'view_order': component.view_order
            }
            if api:
                component_context.update(component.component.get_api_context_data(request))
            else:
                component_context.update(component.component.get_context_data(request))
            context.append(component_context)
        return context

    def get_components(self):
        context = []
        components = self.pagecomponent_set.filter(component__is_active=True, component__is_deleted=False)
        for component in components:
            context.append(component.component)
        return context

    def admin_link_to_add_component(self):
        link = reverse("admin:garpix_page_basecomponent_add")
        return format_html(
            '<a class="related-widget-wrapper-link add-related addlink" href="{0}?_to_field=id&_popup=1&pages={1}">Добавить компонент</a>',
            link, self.id)

    def get_seo_value(self, field_name, site=None):
        from garpix_page.admin.settings.seo_template import SeoTemplateForm
        from garpix_page.models.settings import SeoTemplate

        site = site or self._default_site

        seo_value_cache = cache_service.get_seo_by_page(self.pk, field_name, site)

        if seo_value_cache is not None:
            return seo_value_cache

        seo_templates = SeoTemplate.active_objects.filter(sites__in=[site]).all()

        for temp in seo_templates:
            is_model_rule = temp.rule_field == SeoTemplateForm.RULE_FIELD.MODEL_NAME and self.__class__.__name__ == temp.model_rule_value
            is_field_rule = temp.rule_field != SeoTemplateForm.RULE_FIELD.MODEL_NAME and str(temp.rule_value) in str(
                getattr(self, temp.rule_field, None))
            if is_model_rule or is_field_rule:
                try:
                    seo_value = getattr(temp, field_name, '').format(**self.get_seo_template_keys())
                except (AttributeError, KeyError, ValueError) as e:
                    # ToDo: добавить предупреждение в админке
                    print(f'{field_name}: {e}')
                    seo_value = getattr(temp, field_name, '')
                break
        else:
            seo_value = getattr(self, field_name, '')

        cache_service.set_seo_by_page(self.pk, field_name, seo_value, site)
        return seo_value or ''

    def get_seo_title(self):
        language_code = translation.get_language()
        return self.get_seo_value(f'seo_title_{language_code}')

    def get_seo_keywords(self):
        language_code = translation.get_language()
        return self.get_seo_value(f'seo_keywords_{language_code}')

    def get_seo_description(self):
        language_code = translation.get_language()
        return self.get_seo_value(f'seo_description_{language_code}')

    def get_seo_author(self):
        language_code = translation.get_language()
        return self.get_seo_value(f'seo_author_{language_code}')

    def get_seo_og_type(self):
        return self.get_seo_value('seo_og_type')

    def get_seo_image(self):
        return self.get_seo_value('seo_image')

    @classmethod
    def url_patterns(cls):
        return {
            '{model_name}': {
                'verbose_name': '{model_title}',
                'pattern': ''
            },
        }

    def get_subpages_list(self):
        patterns = self.url_patterns()
        patterns.pop('{model_name}')
        subpages = {}
        for key, pattern in patterns.items():
            subpages[key] = {'title': pattern['verbose_name'],
                             'absolute_url': f"{self.absolute_url}{pattern['pattern']}"}
        return subpages

    def get_subpage_url(self, subpage_key=None, subpage_params=None):
        subpage_key = subpage_key or self.subpage_key
        if subpage_key:
            parameters = subpage_params or self.subpage_params
            sub_page_url = self.url_patterns()[subpage_key]['pattern'].replace('<', '%(').replace('>',
                                                                                                  ')s') % parameters
            return f"{self.get_absolute_url()}{sub_page_url}"
        return ''


@receiver(pre_save)
def reset_url(sender, instance: BasePage, update_fields, **kwargs):
    if type(sender) == type(BasePage):
        if instance.seo_title is None:
            instance.seo_title = instance.title

        if instance.pk:

            cache_service.clear_seo_data(instance.pk)
            old_instance = BasePage.objects.get(pk=instance.pk)
            if instance.parent != old_instance.parent or instance.slug != old_instance.slug:

                instance.set_url()
                children = instance.get_children()
                if children:
                    if len(children) > getattr(settings, 'GARPIX_PAGE_CHILDREN_LEN', 10):
                        clear_child_cache.delay(instance.id)
                    else:
                        pages_to_update = []
                        set_children_url(instance, children, pages_to_update)

                        BasePage.objects.bulk_update(pages_to_update, ['url'])
                        BasePage.objects.rebuild()

        else:
            instance.set_url()


@receiver(pre_delete)
def update_children_url(sender, instance: BasePage, *args, **kwargs):
    if type(sender) == type(BasePage):
        children = instance.get_children()
        if children:
            pages_to_update = []
            set_children_url(None, children, pages_to_update)

            BasePage.objects.bulk_update(pages_to_update, ['url'])
            BasePage.objects.rebuild()
