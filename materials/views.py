from typing import Any

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from materials import serializers
from materials.models import Course, Lesson, Subscription
from materials.paginators import ListPagination
from materials.permissions import IsModeratorUser, IsOwnerUser
from materials.tasks import notify_users

docs_response = openapi.Response("Создание/удаление подписки по запросу", serializers.Subscribe)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = ListPagination

    def perform_create(self, serializer: BaseSerializer) -> Any:
        """Назначение владельца при создании курса"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer: BaseSerializer) -> Any:
        """Вызов оповещения пользователей при обновлении курса"""
        super().perform_update(serializer)
        notify_users.delay(serializer.data["id"], serializer.data["name"])

    def get_permissions(self) -> Any:
        """Права доступа в зависимости от действия"""
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModeratorUser]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwnerUser]
        elif self.action in ("update", "partial_update", "retrieve"):
            self.permission_classes = [IsAuthenticated, IsOwnerUser | IsModeratorUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Фильтрация чужих курсов из списка"""
        user = request.user
        if user.groups.filter(name="Moderators").exists() or user.is_superuser:
            queryset = self.get_queryset()
        else:
            queryset = self.get_queryset().filter(owner=user)
        # Востановление пагинации
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class LessonList(generics.ListAPIView):
    serializer_class = serializers.LessonSerializer
    pagination_class = ListPagination

    def get_queryset(self) -> Any:
        """Фильтрация чужих уроков из списка"""
        user = self.request.user
        if user.groups.filter(name="Moderators").exists() or user.is_superuser:
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieve(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerUser | IsModeratorUser]


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModeratorUser]

    def perform_create(self, serializer: BaseSerializer) -> Any:
        """Назначение владельца при создании урока"""
        serializer.save(owner=self.request.user)


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerUser | IsModeratorUser]

    def perform_update(self, serializer: BaseSerializer) -> Any:
        """Вызов оповещения пользователей при обновлении курса"""
        super().perform_update(serializer)
        course = Course.objects.get(pk=serializer.data["course"])
        notify_users.delay(course.pk, course.name)


class LessonDestroy(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerUser]


class SubscriptionsList(generics.ListAPIView):
    serializer_class = serializers.SubscriptionSerializer

    def get_queryset(self) -> Any:
        """Фильтрация чужих подписок из списка"""
        user = self.request.user
        if user.groups.filter(name="Moderators").exists() or user.is_superuser:
            return Subscription.objects.all()
        return Subscription.objects.filter(user=user)


class CourseSubscribe(generics.GenericAPIView):
    queryset = Subscription.objects.all()
    serializer_class = serializers.Subscribe

    @swagger_auto_schema(responses={200: docs_response})
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Создание/удаление подписки по запросу"""
        user = self.request.user
        course_pk = self.kwargs.get("course_pk")
        course = generics.get_object_or_404(Course.objects.all(), pk=course_pk)
        subscription = self.get_queryset().filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
