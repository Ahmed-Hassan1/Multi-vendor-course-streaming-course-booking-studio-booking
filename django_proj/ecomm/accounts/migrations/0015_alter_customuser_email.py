# Generated by Django 3.2.13 on 2022-06-04 09:42
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20220604_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, verbose_name='email address'),
            preserve_default=False,
        ),
    ]
