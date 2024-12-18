# Generated by Django 5.0.6 on 2024-10-22 03:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
        ('vendorapp', '0014_rename_product_images_product_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendorapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.usermodel')),
            ],
        ),
    ]
