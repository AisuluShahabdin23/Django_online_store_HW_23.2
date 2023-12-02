# Generated by Django 4.2.6 on 2023-10-25 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Category name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Product name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='db_store/', verbose_name='Picture')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Product price')),
                ('creation_date', models.DateField(auto_now_add=True, verbose_name='Creation date')),
                ('changing_date', models.DateField(auto_now=True, verbose_name='Last changed date')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Category name')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
