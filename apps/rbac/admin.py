# from django.contrib import admin
# from apps.products.models import Product, Category, SubCategory

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(SubCategory)

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from apps.accounts.models import User

# admin.site.register(User, UserAdmin)

from django.contrib import admin
from apps.rbac.models import Role, Permission

admin.site.register(Role)
admin.site.register(Permission)
