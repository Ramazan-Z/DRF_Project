from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import Pyment, User


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.client.force_authenticate(user=self.user)

    def test_users_list(self) -> None:
        """Тест списка пользователей"""
        url = reverse("users:users-list")
        expected_response = [
            {
                "id": self.user.pk,
                "email": "user@sky.pro",
                "username": "user",
                "sity": None,
                "avatar": None,
            }
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_user(self) -> None:
        """Тест одного пользователя"""
        url = reverse("users:users-detail", args=(self.user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("id"), self.user.pk)

    def test_user_register(self) -> None:
        """Тест регистрации пользователя"""
        url = reverse("users:users-list")
        data = {
            "email": "user2@sky.pro",
            "username": "user2",
            "password": "user2",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self) -> None:
        """Тест редактирования профиля"""
        url = reverse("users:users-detail", args=(self.user.pk,))
        data = {
            "last_name": "new_last_name",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.pk).last_name, data["last_name"])

    def test_user_delete(self) -> None:
        """Тест удаления пользователя"""
        url = reverse("users:users-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)


class PaymentsTestCase(APITestCase):

    def setUp(self) -> None:
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.course = Course.objects.create(name="course", description="course_description", owner=self.user)
        self.pyment = Pyment.objects.create(user=self.user, course=self.course, amount=1000)
        self.client.force_authenticate(user=self.user)

    def test_payments_list(self) -> None:
        """Тест списка платежей"""
        url = reverse("users:pyments-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
