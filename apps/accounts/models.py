from django.contrib.auth.models import AbstractUser
from django.db import models

## original
# class User(AbstractUser):
#     is_verified = models.BooleanField(default=False)


# class User(AbstractUser):
#     email = models.EmailField(unique=True) #if email is already theree then migration may fail,clean data or remove unique constraint and add later
#     role = models.ForeignKey("accounts.Role", on_delete=models.SET_NULL, null=True)# this creates role_id in db
#     is_verified = models.BooleanField(default=False)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField("rbac.Role", related_name="users")
    is_verified = models.BooleanField(default=False)


# RolePermission table	✅ ManyToMany
# UserRole table	✅ ManyToMany
# No permission code	✅ unique code
# duplicate risk	❌ removed


# class User(AbstractUser):
#     email = models.EmailField(unique=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["username"]

#     def __str__(self):
#         return self.email
