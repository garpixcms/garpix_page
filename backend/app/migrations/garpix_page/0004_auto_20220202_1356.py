# Generated by Django 3.1 on 2022-02-02 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0003_auto_20220201_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basepagecomponent',
            name='pages',
            field=models.ManyToManyField(blank=True, related_name='components', to='garpix_page.BasePage', verbose_name='Страницы для отображения'),
        ),
    ]
