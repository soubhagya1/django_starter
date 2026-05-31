from django.contrib import admin
from apps.products.models import Product, Category, SubCategory

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)

# above code-
# Django Admin auto-generates:

# Create form
# Update form
# Delete option
# List view


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "price")
