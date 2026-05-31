# from django.views.generic import ListView
from django.http import JsonResponse
from apps.products.models.product import Product
from apps.products.services.product_service import product_create
from apps.products.selectors.product_selector import get_all_products

from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from apps.products.serializers.product_serializer import ProductSerializer
from apps.products.throttles import ProductListThrottle
from apps.rbac.permissions import (
    CanCreateProduct,
    CanViewProduct,
    CanUpdateProduct,
    CanDeleteProduct,
)
from apps.rbac.services.permission_service import has_permission
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django_ratelimit.decorators import ratelimit
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
import logging

logger = logging.getLogger(__name__)
# from rest_framework.throttling import ScopedRateThrottle

# from ..models import Product

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import ProductForm, ManufacturingForm, OwnerForm


# class ProductListView(ListView):
#     model = Product
#     paginate_by = 10
#     template_name = "product/list.html"


# below two function work
# def product_list(request):
#     products = get_all_products()
#     data = list(products.values())
#     return JsonResponse(data, safe=False)


# # def product_create(request):
# def create_product(request):
#     if request.method == "POST":
#         data = {
#             "name": request.POST.get("name"),
#             "price": request.POST.get("price"),
#             "subcategory_id": request.POST.get("subcategory_id"),
#         }
#         product = product_create(data)
#         return JsonResponse({"id": product.id})


# below fucntion are api view,now instead of putting logic in views we are putting logic in services and selectors


@api_view(["GET"])
# @permission_classes(
#     [AllowAny]
# )  # Allow any user (authenticated or not) to access this view
# @permission_classes([IsAuthenticated])
@ratelimit(key="ip", rate="5/m", block=True)
def product_list(request):
    # products = Product.objects.all()
    products = get_all_products()
    serializer = ProductSerializer(products, many=True)
    # return Response(serializer.data)
    return Response({"success": True, "data": serializer.data})


class HasProductCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "create_product")


# class ProductListAPIView(APIView):
#     def get(self, request):
#         products = get_all_products()
#         serializer = ProductSerializer(products, many=True)
#         # return Response(serializer.data)
#         return Response({"success": True, "data": serializer.data})


# non enterprise style approche
@api_view(["POST"])
# def product_create(request):
def create_product(request):
    logger.info(f"Creating product: {request.data.get('name')}")
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        product = product_create(serializer.validated_data)
        # serializer.save()
        # return Response(serializer.data)
        # return Response(ProductSerializer(product).data)
        return Response({"success": True, "data": ProductSerializer(product).data})
    logger.info(f"Product created successfully with id {product.id}")
    return Response(serializer.errors, status=400)


# enterprise style approche
# class ProductCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         if not has_permission(request.user, "create_product"):
#             return Response({"error": "Permission denied"}, status=403)

#         return Response({"success": True})


# enterprise style approche
# class ProductCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     # permission_classes = [IsAuthenticated, HasProductCreatePermission]

#     def post(self, request):
#         # 🔐 RBAC check
#         if not has_permission(request.user, "create_product"):
#             return Response(
#                 {"success": False, "error": "Permission denied"}, status=403
#             )

#         # 📦 Validate input
#         serializer = ProductSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response({"success": False, "errors": serializer.errors}, status=400)

#         # 🧠 Business logic
#         product = product_create(serializer.validated_data)

#         # 📤 Response
#         return Response(
#             {"success": True, "data": ProductSerializer(product).data}, status=201
#        # )


# more enterprise style approche-
# class ProductCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated, CanCreateProduct]
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             product = create_product(
#                 serializer.validated_data, user=request.user
#             )  # inject user here and handle it in service layer
#             return Response(
#                 {"success": True, "data": ProductSerializer(product).data}, status=201
#             )
#         return Response(serializer.errors, status=400)


# final enterprise style approche with separate permission class and handling user in service layer
# @extend_schema(
#     tags=["Products"],
#     summary="Create Product",
#     description="Creates a new product with category and subcategory.",
#     examples=[
#         OpenApiExample(
#             "Create Product Example",
#             value={
#                 "name": "iPhone",
#                 "description": "Apple phone",
#                 "category": 1,
#                 "subcategory": 1,
#                 "price": 80000,
#             },
#             request_only=True,
#         ),
#     ],
# )
@extend_schema(
    tags=["Products"],
    summary="Create Product",
    description="Creates a new product.",
    request=ProductSerializer,  # Without it, Swagger often cannot build request schema/examples correctly for plain APIViews.
    responses={
        201: ProductSerializer,
    },
    examples=[
        OpenApiExample(
            "Create Product Example",
            value={
                "name": "iPhone 15",
                "description": "Apple flagship phone",
                "category": 1,
                "subcategory": 1,
                "price": 80000,
                "is_active": True,
            },
            request_only=True,
        )
    ],
)
class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, CanCreateProduct]
    parser_classes = [MultiPartParser, FormParser]
    # throttle_classes = [ScopedRateThrottle, UserRateThrottle]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = "products_create"

    def post(self, request):
        logger.info(f"Product create API hit by user {request.user.id}")
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=400)

        try:
            with transaction.atomic():
                product = product_create(
                    serializer.validated_data, user=request.user
                )  # not create_product

            return Response(
                {"success": True, "data": ProductSerializer(product).data}, status=201
            )

        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)


# for better documentation in swagger ui
@extend_schema(
    tags=["Products"],
    summary="List Products",
    description="Returns paginated list of products with optional search and price filtering.",
)
class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated, CanViewProduct]
    # throttle_classes = [UserRateThrottle] #this is global but below is throtltling for this api only
    throttle_classes = [ProductListThrottle]

    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'products_list'
    # def get(self, request):
    #     products = get_all_products()
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)

    def get(self, request):
        logger.info(f"Product list API hit by user: {request.user.id}")
        # filters = {
        #     "min_price": request.GET.get("min_price"),
        #     "max_price": request.GET.get("max_price"),
        # }
        filters = {
            "search": request.GET.get("search"),
            "min_price": request.GET.get("min_price"),
            "max_price": request.GET.get("max_price"),
        }

        # products = get_all_products()
        products = get_all_products(filters)  # /products?min_price=100&max_price=500

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(page, many=True)
        # return paginator.get_paginated_response(serializer.data)
        return Response(
            {
                "success": True,
                "count": paginator.page.paginator.count,
                "results": serializer.data,
            }
        )


class ProductUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, CanUpdateProduct]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})

        return Response(serializer.errors, status=400)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, CanDeleteProduct]

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"success": True})


# User → multiple Roles
# Role → multiple Permissions
# Permission → checked via code


# @login_required
# def product_create(request):
#     if request.method == "POST":
#         product_form = ProductForm(request.POST, request.FILES)
#         manufacturing_form = ManufacturingForm(request.POST)
#         owner_form = OwnerForm(request.POST)

#         if all(
#             [
#                 product_form.is_valid(),
#                 manufacturing_form.is_valid(),
#                 owner_form.is_valid(),
#             ]
#         ):
#             product = product_form.save(commit=False)
#             product.user = request.user
#             product.save()

#             manufacturing = manufacturing_form.save(commit=False)
#             manufacturing.product = product
#             manufacturing.save()

#             owner = owner_form.save(commit=False)
#             owner.product = product
#             owner.save()

#             return redirect("dashboard")

#     else:
#         product_form = ProductForm()
#         manufacturing_form = ManufacturingForm()
#         owner_form = OwnerForm()

#     return render(
#         request,
#         "product/create.html",
#         {
#             "product_form": product_form,
#             "manufacturing_form": manufacturing_form,
#             "owner_form": owner_form,
#         },
#     )
