# Generated by Django 5.1 on 2024-08-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
