from apps.products.models import Product
from django.core.cache import cache
from django.db.models import Q

# def get_all_products():
#     return Product.objects.all()

# with no filter
# def get_all_products():
#     return Product.objects.select_related("subcategory").all()


# with filter
# def get_all_products(filters=None):
#     qs = Product.objects.select_related("subcategory")

#     if filters:
#         if filters.get("search"):
#             qs = qs.filter(Q(name__icontains=filters["search"]))
#         if filters.get("min_price"):
#             qs = qs.filter(price__gte=filters["min_price"])

#         if filters.get("max_price"):
#             qs = qs.filter(price__lte=filters["max_price"])

#     return qs


# with filter and redis caching
def get_all_products(filters=None):
    cache_key = f"products:{filters}"
    # data = cache.get(cache_key)
    # if data:
    #     # print("Cache hit")
    #     return data

    # cached_ids = cache.get(cache_key)
    # below code is to handle case when redis is down, we dont want our app to crash, we will just return data from db without caching
    try:
        cached_ids = cache.get(cache_key)
    except Exception:
        cached_ids = None

    if cached_ids:
        print("Cache hit")
        return Product.objects.filter(id__in=cached_ids)

    # qs = Product.objects.select_related("subcategory").all()
    print("cache miss")
    # Pagination unordered queryset is not good because it can return duplicate data in different pages, so we need to order it by some field, here we are ordering it by created_at field in descending order, so that we get latest products first and we dont get duplicate data in different pages
    qs = Product.objects.select_related("subcategory").all().order_by("-created_at")

    # remove .all() if you want to return queryset instead of list, we are returning queryset because we want to apply pagination on it later, if we return list then we have to do pagination in memory which is not efficient
    if filters:
        if filters.get("search"):
            qs = qs.filter(Q(name__icontains=filters["search"]))
        if filters.get("min_price"):
            qs = qs.filter(price__gte=filters["min_price"])

        if filters.get("max_price"):
            qs = qs.filter(price__lte=filters["max_price"])
    # data = list(qs.values())
    ids = list(
        qs.values_list("id", flat=True)
    )  # we are caching only ids to save space, we can cache full data if we want
    # cache.set(cache_key, data, timeout=60)  # cache for 60 seconds

    ## cache.set(cache_key, ids, timeout=60)  # cache for 60 seconds
    # return data
    try:
        cache.set(cache_key, ids, timeout=60)
    except Exception:
        pass

    return qs


def get_product_by_id(product_id: int):
    return Product.objects.filter(id=product_id).first()


# def get_all_products():
#     return Product.objects.select_related("category").all()
