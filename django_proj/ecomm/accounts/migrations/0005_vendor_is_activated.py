# Generated by Django 3.2.12 on 2022-04-09 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_comapny_name_vendor_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='is_activated',
            field=models.BooleanField(default=False),
        ),
    ]