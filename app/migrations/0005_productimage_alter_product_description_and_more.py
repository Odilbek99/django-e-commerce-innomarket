# Generated by Django 4.1.3 on 2022-11-13 13:49

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_section_alter_subcategory_category_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_info',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.DeleteModel(
            name='ProdectImage',
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='app.product'),
        ),
    ]
