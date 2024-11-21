from typing import Any

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Pyment, User


class Command(BaseCommand):
    help = "Clear test data from data base"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        User.objects.all().delete()
        Group.objects.all().delete()
        Pyment.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("The data has been successfully deleted from the database"))
