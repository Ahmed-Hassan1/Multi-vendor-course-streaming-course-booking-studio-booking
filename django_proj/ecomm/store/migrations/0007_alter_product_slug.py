# Generated by Django 3.2.12 on 2022-03-27 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20220327_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
