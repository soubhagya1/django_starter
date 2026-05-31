# from rest_framework import serializers
from rest_framework import serializers
from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # to make image optional

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = [
            "user"
        ]  # ✅ important to prevent user from being set via API & prevents "user is required"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
