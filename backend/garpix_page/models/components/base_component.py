from django.db import models
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey, PolymorphicMPTTModelManager
from django.urls import reverse
from django.utils.html import format_html
from ...models import BasePage


class PageComponent(models.Model):
    component = models.ForeignKey("BaseComponent", on_delete=models.CASCADE)
    page = models.ForeignKey("BasePage", on_delete=models.CASCADE)
    view_order = models.IntegerField(default=1)

    class Meta:
        unique_together = (('component', 'page'),)
        ordering = ('view_order', )


class BaseComponent(PolymorphicMPTTModel):
    """
    Базовый компонент
    """
    title = models.CharField(max_length=255, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    limit = models.Q(app_label='garpix_page', model='BasePage') | models.Q(
        app_label='garpix_page', model='self')

    parent = PolymorphicTreeForeignKey('self', null=True, blank=True, related_name='children',
                                       db_index=True, verbose_name='Родительский компонент', on_delete=models.SET_NULL,
                                       limit_choices_to={})
    pages = models.ManyToManyField(BasePage, blank=True, related_name='components', through='PageComponent',
                                   verbose_name='Страницы для отображения')

    front_info = models.ForeignKey('FrontInfo', on_delete=models.SET_NULL, verbose_name='Информация для фронта',
                                   blank=True, null=True)

    text_title = models.CharField(blank=True, default='', max_length=128, verbose_name='Заголовок')
    objects = PolymorphicMPTTModelManager()

    template = 'garpix_page/components/default.html'
    searchable_fields = ('title',)
    serializer = None  # default is generator of serializers: garpix_page.serializers.serializer.get_serializer

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
        ordering = ('created_at', 'title',)

    def __str__(self):
        return self.title

    def model_name(self):
        return self.get_real_instance_class()._meta.verbose_name  # noqa

    model_name.short_description = 'Тип'

    @classmethod
    def is_for_component_view(cls):
        return True

    @property
    def admin_link_to_change(self):
        link = reverse(f"admin:garpix_page_basecomponent_change",
                       args=[self.id])
        return format_html('<a class="inlinechangelink" href="{0}">{1}</a>', link, self.title)

    def get_serializer(self):
        return None
