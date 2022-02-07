# Generated by Django 3.1 on 2022-02-04 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0004_auto_20220202_1356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sliderpagecomponent',
            name='basepagecomponent_ptr',
        ),
        migrations.RemoveField(
            model_name='textdescriptionpagecomponent',
            name='basepagecomponent_ptr',
        ),
        migrations.RemoveField(
            model_name='textimagepagecomponent',
            name='basepagecomponent_ptr',
        ),
        migrations.RemoveField(
            model_name='textpagecomponent',
            name='basepagecomponent_ptr',
        ),
        migrations.DeleteModel(
            name='ImagePageComponent',
        ),
        migrations.DeleteModel(
            name='SliderPageComponent',
        ),
        migrations.DeleteModel(
            name='TextDescriptionPageComponent',
        ),
        migrations.DeleteModel(
            name='TextImagePageComponent',
        ),
        migrations.DeleteModel(
            name='TextPageComponent',
        ),
    ]
