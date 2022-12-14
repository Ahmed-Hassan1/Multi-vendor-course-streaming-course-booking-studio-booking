# Generated by Django 3.2.13 on 2022-08-16 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_remove_customuser_username'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursestudent',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer'),
        ),
        migrations.CreateModel(
            name='CourseSessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_hour', models.CharField(max_length=20)),
                ('end_hour', models.CharField(max_length=20)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.AddField(
            model_name='coursestudent',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.coursesessions'),
        ),
    ]
