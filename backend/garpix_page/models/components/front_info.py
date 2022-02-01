from django.db import models
from garpix_utils.file import get_file_path

class FrontInfo(models.Model):
    type = models.CharField(max_length=128, verbose_name='Тип')
    short_description = models.TextField(verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Полное описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Информация для фронта'
        verbose_name_plural = 'Информация для фронта'
        ordering = ('created_at', )


class FrontInfoScreenshots(models.Model):
    screenshot = models.ImageField(verbose_name='Скриншот', upload_to=get_file_path)
    front_info = models.ForeignKey(FrontInfo, on_delete=models.CASCADE, verbose_name='Информация для фронта',
                                   related_name='front_info_screenshots')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Скриншот информации для фронта'
        verbose_name_plural = 'Скриншоты информации для фронта'
        ordering = ('front_info', 'created_at')
