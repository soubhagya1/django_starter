from django.urls import reverse
from rest_framework.test import APIClient
import pytest

pytestmark = pytest.mark.django_db


# @pytest.mark.django_db for individual marking
def test_register_api():
    client = APIClient()

    response = client.post(
        # "/api/register/",
        reverse("api_register"),
        {
            "username": "newuser",
            "email": "new@example.com",
            "password": "Password123",
        },
        format="json",
    )

    # print(response.data)
    # print(response.status_code)

    assert response.status_code == 201
