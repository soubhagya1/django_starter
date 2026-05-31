from django.urls import path

# from .views import ProductListView

# from .services.product_create import product_create
# from apps.products.services.product_service import product_create
# from .views.product_views import product_list  # , create_product
from .views.product_views import (
    ProductCreateAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
    ProductListAPIView,
)

urlpatterns = [
    # path("create/", product_create, name="product_create"),
    # path("", ProductListView.as_view(), name="product_list"),
    # path("", product_list),
    path("", ProductListAPIView.as_view(), name="product_list"),
    # path("create/", create_product),
    # path("create", ProductCreateAPIView.as_view()),
    path(
        "create/",
        ProductCreateAPIView.as_view(),
        name="product_create",
    ),
    path("<int:pk>/update/", ProductUpdateAPIView.as_view()),
    path("<int:pk>/delete/", ProductDeleteAPIView.as_view()),
]
