# apps/core/cache.py

from django.core.cache import cache


def clear_product_cache():
    if hasattr(cache, "delete_pattern"):
        cache.delete_pattern("products:*")
    else:
        cache.clear()
