# Generated by Django 5.0.3 on 2024-08-28 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0005_profile_reference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
    ]
