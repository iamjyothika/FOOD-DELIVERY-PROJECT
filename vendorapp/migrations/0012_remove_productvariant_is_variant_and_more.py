# Generated by Django 5.0.6 on 2024-10-18 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorapp', '0011_productvariant_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='is_variant',
        ),
        migrations.AddField(
            model_name='productvariant',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='salesprice',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
