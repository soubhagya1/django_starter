from django.urls import reverse

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import User
from apps.rbac.models import (
    Role,
    Permission,
    # RolePermission,
    # UserRole,
)

pytestmark = pytest.mark.django_db

# below are in conftest.py, so commented here
# @pytest.fixture
# def user():
#     return User.objects.create_user(
#         username="testuser",
#         password="password123",
#     )


# @pytest.fixture
# def authenticated_client(user):
#     refresh = RefreshToken.for_user(user)

#     client = APIClient()

#     client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

#     return client


# def test_user_without_permission_cannot_view_products(
#     authenticated_client,
# ):
#     response = authenticated_client.get("/products/")

#     assert response.status_code == 403


# @pytest.fixture
# def user_role():
#     return Role.objects.create(name="User")


# @pytest.fixture
# def view_product_permission():
#     return Permission.objects.create(
#         code="view_product",
#         name="View Product",
#     )


# @pytest.fixture
# def role_with_permission(
#     user_role,
#     view_product_permission,
# ):
#     user_role.permissions.add(view_product_permission)

#     return user_role


# @pytest.fixture
# def user_with_view_permission(
#     user,
#     role_with_permission,
# ):
#     user.roles.add(role_with_permission)

#     return user


def test_user_can_view_products(
    authenticated_client,
    user_with_view_permission,
):
    # response = authenticated_client.get("/products/")
    response = authenticated_client.get(reverse("product_list"))

    assert response.status_code == 200
