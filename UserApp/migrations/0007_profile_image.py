# Generated by Django 5.0.3 on 2024-08-28 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0006_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.FileField(null=True, upload_to='customer_image/'),
        ),
    ]
