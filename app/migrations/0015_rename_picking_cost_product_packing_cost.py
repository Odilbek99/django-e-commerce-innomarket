# Generated by Django 4.1.3 on 2022-11-17 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_product_picking_cost_product_tax'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='picking_cost',
            new_name='packing_cost',
        ),
    ]
