# Generated by Django 3.2.13 on 2022-08-22 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_videostream'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VideoStream',
        ),
    ]