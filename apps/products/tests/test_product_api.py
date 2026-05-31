# JWT
# +
# RBAC
# +
# Product API
# +
# Database

import pytest
from apps.products.models import Category, SubCategory, Product
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture
def category():
    return Category.objects.create(name="Electronics")


@pytest.fixture
def subcategory(category):
    return SubCategory.objects.create(
        name="Phones",
        category=category,
    )


def test_print_url():
    print(reverse("product_create"))


def test_product_create(
    authenticated_client,
    category,
    subcategory,
    user_with_view_permission,
    user_with_create_permission,
):
    response = authenticated_client.post(
        # "/products/create/",
        reverse("product_create"),
        {
            "name": "iPhone",
            "description": "Apple phone",
            "price": 80000,
            "category": category.id,
            # "user_id": authenticated_client.handler._force_user.id,
            # "user": user_with_view_permission,
            "subcategory": subcategory.id,
        },
        format="multipart",
    )
    print(response.status_code)
    print(response.data)

    assert response.status_code == 201
    # assert response.status_code == 201


def test_product_list(
    authenticated_client,
    user_with_view_permission,
):
    # response = authenticated_client.get("/api/products/")
    response = authenticated_client.get(reverse("product_list"))

    assert response.status_code == 200

    assert "results" in response.data


def test_product_search(
    authenticated_client,
    user_with_view_permission,
    category,
    subcategory,
):
    Product.objects.create(
        user=user_with_view_permission,
        name="iPhone",
        price=1000,
        category=category,
        subcategory=subcategory,
    )

    # response = authenticated_client.get("/products/?search=iPhone")
    # response = authenticated_client.get("/api/v1/products/?search=iPhone")
    url = reverse("product_list")
    # response = authenticated_client.get(f"{url}?search=iPhone")
    response = authenticated_client.get(
        reverse("product_list"),
        {
            "search": "iPhone",
        },
    )
    assert response.status_code == 200


def test_product_price_filter(
    authenticated_client,
    user_with_view_permission,
):
    # response = authenticated_client.get("/products/?min_price=100")
    url = reverse("product_list")
    response = authenticated_client.get(f"{url}?min_price=100")

    assert response.status_code == 200
