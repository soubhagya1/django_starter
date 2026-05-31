def has_permission(user, permission_code: str):
    if not user.is_authenticated:
        return False

    return user.roles.filter(permissions__code=permission_code).exists()
