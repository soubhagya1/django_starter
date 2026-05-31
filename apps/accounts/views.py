from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.urls import reverse_lazy

from apps.accounts.serializers.account_serializer import RegisterSerializer
from apps.accounts.throttle import LoginThrottle
from .forms import RegisterForm, LoginForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    # success_url = reverse_lazy('dashboard')
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user) commented out to prevent auto-login after registration
        return super().form_valid(form)


# @extend_schema(
#     tags=["Authentication"],
#     summary="Register User",
#     description="Registers a new user account.",
#     examples=[
#         OpenApiExample(
#             "Register Example",
#             value={
#                 "username": "john",
#                 "email": "john@example.com",
#                 "password": "Password123",
#             },
#             request_only=True,
#         ),
#     ],
# )
@extend_schema(
    tags=["Authentication"],
    summary="Register User",
    description="Registers a new user account.",
    request=RegisterSerializer,
    responses={
        201: RegisterSerializer,
    },
    examples=[
        OpenApiExample(
            "Register Example",
            value={
                "username": "john",
                "email": "john@example.com",
                "password": "Password123",
            },
            request_only=True,
        )
    ],
)
class RegisterAPIView(APIView):
    permission_classes = [
        AllowAny
    ]  # "rest_framework.permissions.IsAuthenticated" so every api is protected but we allow this one to be public for registration

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=400)


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    # throttle_classes = [LoginThrottle] thhis is web view throttlt not work

    # next_page = "product_list"
    def get_success_url(self):
        # return reverse_lazy("product_list") #this is product api json so after login it will return json response of products list instead of redirecting to product list page, you can change it to dashboard or any page you want
        # return reverse_lazy("admin:index")
        return "/api/docs/"


# this is for api login with jwt token
@extend_schema(
    tags=["Authentication"],
    summary="Obtain JWT Tokens",
    description="Obtains access and refresh tokens for a user.",
)
class CustomTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginThrottle]


# this is for api login with jwt token
class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = [LoginThrottle]


class CustomLogoutView(LogoutView):
    # pass
    next_page = reverse_lazy("login")


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data["refresh"]

            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response(
                {"success": True},
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
