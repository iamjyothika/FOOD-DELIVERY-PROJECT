# Generated by Django 5.0.6 on 2024-10-16 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0005_singleproductimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleproductimages',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='vendorapp.product'),
        ),
    ]