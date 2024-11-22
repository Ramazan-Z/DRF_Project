from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        call_command("clear_db")
        call_command("loaddata", "fixtures/auth_group.json")
        call_command("loaddata", "fixtures/users.json")
        call_command("loaddata", "fixtures/materials.json")
        call_command("loaddata", "fixtures/payments.json")

        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixtures"))
