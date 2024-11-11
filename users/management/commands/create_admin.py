from typing import Any

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание пользователя с правами администратора"

    def handle(self, *args: Any, **options: Any) -> None:
        user = User.objects.create(email="admin@sky.pro")
        user.set_password("admin")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully created admin user with email {user.email}"))
