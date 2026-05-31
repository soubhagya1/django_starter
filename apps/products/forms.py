from django import forms
from .models import Product, ManufacturingDetails, OwnerDetails


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "subcategory",
            "price",
            "is_active",
            "image",
            "video",
        ]


class ManufacturingForm(forms.ModelForm):
    class Meta:
        model = ManufacturingDetails
        fields = ["country", "city", "production_limit"]


class OwnerForm(forms.ModelForm):
    class Meta:
        model = OwnerDetails
        fields = ["owner_name", "contact_email", "contact_phone"]
