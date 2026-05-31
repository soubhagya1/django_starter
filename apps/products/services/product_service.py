from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from apps.core.cache import clear_product_cache
from apps.products.models.product import Product
from apps.products.models.product import ManufacturingDetails
from apps.products.models.product import OwnerDetails
from ..forms import ProductForm, ManufacturingForm, OwnerForm
from django.core.cache import cache
from apps.products.tasks import send_product_created_email
import logging

logger = logging.getLogger(__name__)


# it has @login_required so it is a view not service,tied to http request and response cycle and uses forms, not reusable in api
@login_required
def product_create_view(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        manufacturing_form = ManufacturingForm(request.POST)
        owner_form = OwnerForm(request.POST)

        if all(
            [
                product_form.is_valid(),
                manufacturing_form.is_valid(),
                owner_form.is_valid(),
            ]
        ):
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()

            manufacturing = manufacturing_form.save(commit=False)
            manufacturing.product = product
            manufacturing.save()

            owner = owner_form.save(commit=False)
            owner.product = product
            owner.save()

            return redirect("dashboard")

    else:
        product_form = ProductForm()
        manufacturing_form = ManufacturingForm()
        owner_form = OwnerForm()

    return render(
        request,
        "product/create.html",
        {
            "product_form": product_form,
            "manufacturing_form": manufacturing_form,
            "owner_form": owner_form,
        },
    )


# below are like service functions, not tied to http request and response cycle, reusable in api and views both
# def product_create(data, user):
#     """
#     Simple API service (only Product)
#     """
#     return Product.objects.create(user=user, **data)


# same as above but with cache clearing, if dont use this data becomes stale
# def create_product(data, user):
def product_create(data, user):
    logger.info(f"Creating product: {data.get('name')}")
    product = Product.objects.create(user=user, **data)
    # async task example
    # send_product_created_email.delay(product.id)  # async email sending
    send_product_created_email.delay(product.id, user.email)
    # celery -A config worker --loglevel=info ,in a new terminal to start worker, make sure redis server is running, you can check it by running redis-cli ping in terminal, it should return PONG
    # ❗ clear cache after create
    # below works for redis not locmemvache, for locmemcache we can use cache.clear() but it will clear all cache, so be careful with that in production
    # cache.delete_pattern("products:*")
    clear_product_cache()
    logger.info(f"Product created successfully with id {product.id}")
    return product


# if you need to save category
# def product_create(data, user):
#     subcategory = data.get("subcategory")
#     category = subcategory.category

#     return Product.objects.create(
#         user=user,
#         category=category,  # manual
#         **data
#     )


def product_create_with_details(product_data, manufacturing_data, owner_data, user):
    """
    Advanced service (Product + related models)
    """
    with transaction.atomic():
        product = Product.objects.create(user=user, **product_data)

        ManufacturingDetails.objects.create(product=product, **manufacturing_data)
        OwnerDetails.objects.create(product=product, **owner_data)

    return product
