import pytest
from apps.accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient


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
def refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)


@pytest.fixture
def authenticated_client(user, access_token):
    client = APIClient()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return client
