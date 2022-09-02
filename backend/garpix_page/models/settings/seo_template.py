from django.db import models
from garpix_utils.file import get_file_path


class SeoTemplate(models.Model):

    rule_field = models.CharField(verbose_name='Поле', max_length=255)

    model_rule_value = models.CharField(verbose_name='Название', null=True, blank=True, max_length=255)
    rule_value = models.CharField(verbose_name='Значение', null=True, blank=True, max_length=255)

    seo_title = models.CharField(max_length=250, verbose_name='SEO заголовок страницы (title)', blank=True, default='')
    seo_keywords = models.CharField(max_length=250, verbose_name='SEO ключевые слова (keywords)', blank=True,
                                    default='')
    seo_description = models.TextField(verbose_name='SEO описание (description)', blank=True, default='')
    seo_author = models.CharField(max_length=250, verbose_name='SEO автор (author)', blank=True, default='')
    seo_og_type = models.CharField(max_length=250, verbose_name='SEO og:type', blank=True, default="website")
    seo_image = models.FileField(upload_to=get_file_path, blank=True, null=True, verbose_name='SEO изображение')

    class Meta:
        verbose_name = 'Шаблон для seo'
        verbose_name_plural = 'Шаблоны для seo'
