from catalog.models import Category
from config.settings import CACHE_ENABLED
from django.core.cache import cache


def cache_category():
    if CACHE_ENABLED:
        key = f'category_list'          # Ключ для хранения
        category_list = cache.get(key)  # Получение данных
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()
    return category_list
