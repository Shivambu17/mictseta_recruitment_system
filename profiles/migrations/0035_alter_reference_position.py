# Generated by Django 4.2.15 on 2024-09-20 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0034_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='position',
            field=models.CharField(max_length=60, null=True),
        ),
    ]