# Generated by Django 5.0.6 on 2024-10-17 04:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0007_alter_singleproductimages_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singleproductimages',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='single_images', to='vendorapp.product'),
        ),
    ]
