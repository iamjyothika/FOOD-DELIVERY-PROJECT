# Generated by Django 5.0.6 on 2024-10-17 06:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0010_productvariant_variantproductimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendorapp.vendor'),
        ),
    ]
