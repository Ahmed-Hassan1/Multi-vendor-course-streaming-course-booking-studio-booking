# Generated by Django 3.2.13 on 2022-08-22 09:04

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20220817_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesessions',
            name='course',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='courseCategory', chained_model_field='courseCategory', on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
    ]
