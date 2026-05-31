import pytest

from apps.rbac.models import (
    Role,
    Permission,
    # RolePermission,
    # UserRole,
)
from apps.accounts.models import User

# @pytest.fixture
# def user():
#     return User.objects.create_user(
#         username="testuser",
#         password="password123",
#     )


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="password123",
    )


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


# permission check should be like-
# request.user.roles.filter(
#     permissions__code="view_product"
# ).exists()


def test_user_can_view_products(
    authenticated_client,
    user_with_view_permission,
):
    response = authenticated_client.get("/products/")

    assert response.status_code == 200


def test_user_without_permission_cannot_view_products(
    authenticated_client,
):
    response = authenticated_client.get("/products/")

    assert response.status_code == 403


# @pytest.fixture
# def role_with_view_permission(
#     user_role,
#     view_product_permission,
# ):
#     user_role.permissions.add(
#         view_product_permission
#     )

#     return user_role


# @pytest.fixture
# def user_with_view_permission(
#     user,
#     role_with_view_permission,
# ):
#     UserRole.objects.create(
#         user=user,
#         role=role_with_view_permission,
#     )

#     return user


# @pytest.fixture
# def role_permission(
#     user_role,
#     view_product_permission,
# ):
#     return RolePermission.objects.create(
#         role=user_role,
#         permission=view_product_permission,
#     )


# @pytest.fixture
# def user_with_view_permission(
#     user,
#     user_role,
#     role_permission,
# ):
#     UserRole.objects.create(
#         user=user,
#         role=user_role,
#     )

#     return user


def test_user_can_view_products(
    authenticated_client,
    user_with_view_permission,
):
    response = authenticated_client.get("/products/")

    assert response.status_code == 200


def test_user_without_permission_cannot_view_products(
    authenticated_client,
):
    response = authenticated_client.get("/products/")

    assert response.status_code == 403
