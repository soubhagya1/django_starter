from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from config.settings.base import BASE_DIR
# from config.settings.base import MEDIA_URL
# from config.settings.base import MEDIA_ROOT
from rest_framework.routers import DefaultRouter

# from apps.core.api_views import ItemViewSet
# from apps.core.views import DashboardView, ItemListView
from apps.accounts.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    RegisterAPIView,
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
)

from django.conf import settings

# from config.settings.base import settings

from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
# router.register(r"items", ItemViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    # app
    # path("", DashboardView.as_view(), name="dashboard"),
    # path("items/", ItemListView.as_view(), name="items"),
    # path("api/", include(router.urls)),versioning
    # path(
    #     "api/token/",
    #     CustomTokenObtainPairView.as_view(),
    #     name="custom_token_obtain_pair",
    # ),versioning
    # path(
    #     "api/token/refresh/",
    #     CustomTokenRefreshView.as_view(),
    #     name="custom_token_refresh",
    # ),versioning
    # path("api/register/", RegisterAPIView.as_view(), name="api_register"),versning
    # path("products/", include("apps.products.urls")),versioning
    path("api/v1/", include("config.api_v1_urls")),
    # auth
    # for jwt authentication
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(authentication_classes=[], permission_classes=[]),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
