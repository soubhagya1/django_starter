# Create your models here.
from django.db import models

from django.conf import settings

from apps.products.models.category import Category
from apps.products.models.sub_category import SubCategory

# from config.settings.base import settings

User = (
    settings.AUTH_USER_MODEL
)  # AUTH_USER_MODEL returns string: "accounts.User", Django resolves it internally


# 🔹 MAIN PRODUCT
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    description = models.TextField()

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )  # you dont need this this is bad design, you can get category from subcategory with product.subcat.cat, you are creating redundant data and possibility of inconsistency
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)

    # media
    image = models.ImageField(upload_to="products/images/", null=True, blank=True)
    video = models.FileField(upload_to="products/videos/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 🔹 MANUFACTURING DETAILS
class ManufacturingDetails(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    production_limit = models.IntegerField()


# 🔹 OWNER DETAILS
class OwnerDetails(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    owner_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
