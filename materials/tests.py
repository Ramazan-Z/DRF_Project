from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.course = Course.objects.create(name="course", description="course_description", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="lesson",
            description="lesson_description",
            video_link="https://youtube.com",
            course=self.course,
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self) -> None:
        """Тест списка уроков"""
        url = reverse("materials:lessons-list")
        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "lesson",
                    "description": "lesson_description",
                    "preview": None,
                    "video_link": "https://youtube.com",
                    "course": 1,
                    "owner": 1,
                },
            ],
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_lesson(self) -> None:
        """Тест одного урока"""
        url = reverse("materials:lessons-retrieve", args=(self.lesson.pk,))
        expected_response = {
            "id": 1,
            "name": "lesson",
            "description": "lesson_description",
            "preview": None,
            "video_link": "https://youtube.com",
            "course": 1,
            "owner": 1,
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_lesson_create(self) -> None:
        """Тест создания урока"""
        url = reverse("materials:lessons-create")
        data = {
            "name": "lesson2",
            "description": "lesson_description2",
            "video_link": "https://youtube.com/2/",
            "course": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(Lesson.objects.get(pk=2).owner, self.user)

    def test_lesson_update(self) -> None:
        """Тест редактирования урока"""
        url = reverse("materials:lessons-update", args=(self.lesson.pk,))
        data = {
            "name": "new_name",
            "description": "new_description",
            "video_link": "https://youtube.com/new/",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(pk=self.lesson.pk).name, data["name"])

    def test_lesson_delete(self) -> None:
        """Тест удаления урока"""
        url = reverse("materials:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class CourseTestCase(APITestCase):

    def setUp(self) -> None:
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.course = Course.objects.create(name="course", description="course_description", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="lesson",
            description="lesson_description",
            video_link="https://youtube.com",
            course=self.course,
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_course_list(self) -> None:
        """Тест списка курсов"""
        url = reverse("materials:courses-list")
        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "subscribed": True,
                    "lessons_count": 1,
                    "lessons": [
                        {
                            "id": 1,
                            "name": "lesson",
                            "description": "lesson_description",
                            "preview": None,
                            "video_link": "https://youtube.com",
                            "course": 1,
                            "owner": 1,
                        },
                    ],
                    "name": "course",
                    "description": "course_description",
                    "preview": None,
                    "owner": 1,
                },
            ],
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_course(self) -> None:
        """Тест одного курса"""
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        expected_response = {
            "id": 1,
            "subscribed": True,
            "lessons_count": 1,
            "lessons": [
                {
                    "id": 1,
                    "name": "lesson",
                    "description": "lesson_description",
                    "preview": None,
                    "video_link": "https://youtube.com",
                    "course": 1,
                    "owner": 1,
                },
            ],
            "name": "course",
            "description": "course_description",
            "preview": None,
            "owner": 1,
        }
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_course_create(self) -> None:
        """Тест создания курса"""
        url = reverse("materials:courses-list")
        data = {
            "name": "course2",
            "description": "course_description2",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)
        self.assertEqual(Course.objects.get(pk=2).owner, self.user)

    def test_course_update(self) -> None:
        """Тест редактирования курса"""
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        data = {
            "name": "new_name",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get(pk=self.course.pk).name, data["name"])

    def test_course_delete(self) -> None:
        """Тест удаления курса"""
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):

    def setUp(self) -> None:
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="user@sky.pro", username="user")
        self.course = Course.objects.create(name="course", description="course_description", owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscriptions_list(self) -> None:
        """Тест списка подписок"""
        url = reverse("materials:subscriptions-list")
        expected_response = [
            {
                "id": 1,
                "course": 1,
                "user": 1,
            },
        ]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_response)

    def test_subscribe(self) -> None:
        """Тест создания/отмены подписки"""
        url = reverse("materials:courses-subscribe", args=(self.course.pk,))
        # Отмена подписки
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 0)
        self.assertEqual(response.json(), {"message": "Подписка удалена"})
        # Подписка
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.all().count(), 1)
        self.assertEqual(response.json(), {"message": "Подписка добавлена"})
