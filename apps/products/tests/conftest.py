# import pytest

# from apps.accounts.models import User
# from apps.rbac.models import Role, Permission


# @pytest.fixture
# def user():
#     return User.objects.create_user(
#         username="testuser",
#         password="password123",
#     )


# @pytest.fixture
# def view_product_permission():
#     return Permission.objects.create(
#         code="view_product",
#         name="View Product",
#     )


# @pytest.fixture
# def role_with_view_permission(
#     view_product_permission,
# ):
#     role = Role.objects.create(name="User")

#     role.permissions.add(view_product_permission)

#     return role


# @pytest.fixture
# def user_with_view_permission(
#     user,
#     role_with_view_permission,
# ):
#     user.roles.add(role_with_view_permission)

#     return user

import pytest
from apps.accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from apps.rbac.models import (
    Role,
    Permission,
    # RolePermission,
    # UserRole,
)


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="password123",
    )


@pytest.fixture
def access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.fixture
def authenticated_client(user, access_token):
    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return client


def test_user_without_permission_cannot_view_products(
    authenticated_client,
):
    response = authenticated_client.get("/products/")

    assert response.status_code == 403


@pytest.fixture
def user_role():
    return Role.objects.create(name="User")


@pytest.fixture
def view_product_permission():
    return Permission.objects.create(
        code="view_product",
        name="View Product",
    )


@pytest.fixture
def create_product_permission():
    return Permission.objects.create(
        code="create_product",
        name="Create Product",
    )


@pytest.fixture
def role_with_permission(
    user_role,
    view_product_permission,
):
    user_role.permissions.add(view_product_permission)

    return user_role


@pytest.fixture
def user_with_view_permission(
    user,
    role_with_permission,
):
    user.roles.add(role_with_permission)

    return user


@pytest.fixture
def role_with_create_permission(
    user_role,
    create_product_permission,
):
    user_role.permissions.add(create_product_permission)

    return user_role


@pytest.fixture
def user_with_create_permission(
    user,
    role_with_create_permission,
):
    user.roles.add(role_with_create_permission)

    return user
