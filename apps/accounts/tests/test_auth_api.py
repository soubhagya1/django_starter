# import pytest
# from rest_framework.test import APIClient

# pytestmark = pytest.mark.django_db


# def test_jwt_login():
#     client = APIClient()

#     response = client.post(
#         "/api/token/",
#         {
#             "username": "soubhagya",
#             "password": "soubhagya",
#         },
#         format="json",
#     )

#     assert response.status_code == 200

from django.urls import reverse

import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

# @pytest.mark.django_db


def test_jwt_login(user):
    client = APIClient()

    response = client.post(
        # "/api/token/",
        reverse("custom_token_obtain_pair"),
        {
            "username": "testuser",
            "password": "password123",
        },
        format="json",
    )

    assert response.status_code == 200

    assert "access" in response.data
    assert "refresh" in response.data


def test_invalid_login():
    client = APIClient()

    response = client.post(
        # "/api/token/",
        reverse("custom_token_obtain_pair"),
        {
            "username": "wrong",
            "password": "wrong",
        },
        format="json",
    )

    assert response.status_code == 401


# def test_logout_blacklists_refresh_token(user, refresh_token):
#     client = APIClient()

#     response = client.post(
#         reverse("token_refresh"),
#         {
#             "refresh": refresh_token,
#         },
#     )

#     assert response.status_code == 401


# logout blacklist test
@pytest.mark.django_db
def test_logout_blacklists_refresh_token(
    authenticated_client,
    refresh_token,
):
    response = authenticated_client.post(
        reverse("api_logout"),
        {
            "refresh": refresh_token,
        },
        format="json",
    )

    assert response.status_code == 200


# full test for logout and blacklist
@pytest.mark.django_db
def test_blacklisted_refresh_token_cannot_be_used(
    authenticated_client,
    refresh_token,
):
    authenticated_client.post(
        reverse("api_logout"),
        {
            "refresh": refresh_token,
        },
        format="json",
    )

    response = authenticated_client.post(
        # reverse("token_refresh"),
        reverse("custom_token_refresh"),
        {
            "refresh": refresh_token,
        },
        format="json",
    )

    assert response.status_code == 401
