# Generated by Django 3.2.13 on 2022-05-22 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_delete_vendorpayments'),
        ('store', '0014_auto_20220519_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payemnts', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.vendor')),
            ],
        ),
    ]