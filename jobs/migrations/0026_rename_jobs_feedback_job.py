# Generated by Django 4.2.15 on 2024-09-11 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0025_rename_job_feedback_jobs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='jobs',
            new_name='job',
        ),
    ]
