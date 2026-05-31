# from rest_framework import serializers
from rest_framework import serializers
from apps.accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        # fields = "__all__"
        # read_only_fields = [
        #     "user"
        # ]  # ✅ important to prevent user from being set via API & prevents "user is required"

    # def validate_price(self, value):
    #     if value <= 0:
    #         raise serializers.ValidationError("Price must be positive")
    #     return value
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
