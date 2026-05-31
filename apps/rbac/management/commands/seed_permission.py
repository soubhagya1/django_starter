from django.core.management.base import BaseCommand
from apps.rbac.models import Permission
from apps.rbac.constants import *


class Command(BaseCommand):
    help = "Seed initial permissions"

    def handle(self, *args, **kwargs):
        permissions = [
            (PRODUCT_CREATE, "Create Product"),
            (PRODUCT_VIEW, "View Product"),
            (PRODUCT_UPDATE, "Update Product"),
            (PRODUCT_DELETE, "Delete Product"),
        ]

        for code, name in permissions:
            Permission.objects.get_or_create(code=code, defaults={"name": name})

        self.stdout.write(self.style.SUCCESS("Permissions seeded successfully"))
