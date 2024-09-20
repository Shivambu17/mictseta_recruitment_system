# Generated by Django 4.2.15 on 2024-09-19 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0032_rename_years_of_expreince_workingexpereince_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cover_letter',
            field=models.CharField(default=' ', max_length=225),
        ),
        migrations.AlterField(
            model_name='workingexpereince',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_expereince', to=settings.AUTH_USER_MODEL),
        ),
    ]