# Generated by Django 5.0.3 on 2024-07-25 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0002_product_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='season',
        ),
    ]
