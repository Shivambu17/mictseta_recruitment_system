# Generated by Django 4.2.15 on 2024-09-09 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0017_rename_job_id_jobapplication_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('start_time', models.CharField(max_length=225)),
                ('end_time', models.CharField(max_length=225)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='int_job', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]