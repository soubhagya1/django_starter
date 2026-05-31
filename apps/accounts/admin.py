from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import User


# admin.site.register(User, UserAdmin) #Use the default admin UI provided by Django for the User model.”
# It’s built for default Django User model
# UserAdmin is a class from Django:,It already defines:
# username/password fields
# groups/permissions
# staff/superuser flags
# layout of admin form


# we modified and added roles  and is_verified fields to User model, so we need to customize the admin form to include those fields as well.
# it extends useradmin and adds our custom fields to the form, so we can manage them in the admin interface., filter_hjorizontal is for many-to-many fields to make them easier to use in the admin.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("RBAC", {"fields": ("roles", "is_verified")}),)

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("RBAC", {"fields": ("roles", "is_verified")}),
    )

    filter_horizontal = ("roles",)
    # Without it:
    # roles field looks broken or unusable
    # With it:
    # you get clean multi-select UI
