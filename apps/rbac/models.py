from django.db import models

# class Role(models.Model):
#     name = models.CharField(max_length=100)

# class Permission(models.Model):
#     name = models.CharField(max_length=100)

# class RolePermission(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

# class UserRole(models.Model):
#     user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)

# ❌ No unique constraint → duplicates possible
# ❌ No code field for permission → hard to check in code
# ❌ Manual join tables → Django already handles this better
# ❌ Extra UserRole table → unnecessary unless you need multi-role


# Use ManyToMany instead of manual tables
class Permission(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.code


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(
        Permission, related_name="roles"
    )  # it auto creates rbac_role_permissions table

    def __str__(self):
        return self.name
