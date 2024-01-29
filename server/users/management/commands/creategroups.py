from hmac import new
from users.models import Group
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

GROUPS = {
    "owner": {
        "user": ["add", "change", "delete", "view"],
        "group": ["add", "change", "delete", "view"],
        "category": ["add", "change", "delete", "view"],
        "product": ["add", "change", "delete", "view"],
        "Image": ["add", "change", "delete", "view"],
    },
    "manager": {
        "user": ["add", "change", "view"],
        "group": ["view"],
        "category": ["add", "change", "view"],
        "product": ["add", "change", "view"],
        "Image": ["add", "change", "view"],
    },
    "employee": {
        "user": ["add", "change", "view"],
        "group": ["view"],
        "category": ["change", "view"],
        "product": ["change", "view", "add"],
        "Image": ["change", "view", "add"],
    },
    "customer": {
        "category": ["view"],
        "product": ["view"],
        "Image": ["view"],
    },
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for group, data in GROUPS.items():
            new_group, _ = Group.objects.get_or_create(name=group)

            for model, perms in data.items():
                for perm in perms:
                    name = f"Can {perm} {model}"
                    _perm = Permission.objects.filter(name=name).first()
                    if _perm:
                        new_group.permissions.add(_perm)


# _create_groups()
