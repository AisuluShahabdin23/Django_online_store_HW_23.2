from django.db import models
from django.conf import settings

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category name')
    description = models.TextField(**NULLABLE, verbose_name='Description')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('pk',)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Product name')
    description = models.TextField(**NULLABLE, verbose_name='Description')
    photo = models.ImageField(upload_to='db_store/', **NULLABLE, verbose_name='Picture')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category name')
    price = models.FloatField(**NULLABLE, verbose_name='Product price')
    creation_date = models.DateTimeField(verbose_name='Creation date')
    changing_date = models.DateTimeField(verbose_name='Last changed date', **NULLABLE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.name} ({self.category}) тг.'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('name',)

        permissions = [
            (
                'product_published',
                'Can publish product'
            )
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    number_version = models.IntegerField(verbose_name='Version number')
    title_version = models.CharField(max_length=50, verbose_name='Version name')
    is_active = models.BooleanField(default=True, verbose_name='Current version indicator')

    def __str__(self):
        return f'{self.product} {self.number_version}'

    class Meta:
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
