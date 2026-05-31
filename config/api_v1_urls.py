from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutAPIView,
    RegisterAPIView,
)

urlpatterns = [
    path(
        "token/", CustomTokenObtainPairView.as_view(), name="custom_token_obtain_pair"
    ),
    path(
        "token/refresh/", CustomTokenRefreshView.as_view(), name="custom_token_refresh"
    ),
    path("register/", RegisterAPIView.as_view(), name="api_register"),
    path("products/", include("apps.products.urls")),
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="api_logout",
    ),
]
