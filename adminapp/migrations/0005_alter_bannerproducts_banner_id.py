# Generated by Django 5.0.6 on 2024-10-16 03:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_alter_banner_banner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerproducts',
            name='banner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.banner'),
        ),
    ]
