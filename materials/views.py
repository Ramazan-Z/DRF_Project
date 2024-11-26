from typing import Any

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from materials import serializers
from materials.models import Course, Lesson
from materials.paginators import ListPagination
from materials.permissions import IsModeratorUser, IsOwnerUser


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = ListPagination

    def perform_create(self, serializer: BaseSerializer) -> Any:
        """Назначение владельца при создании курса"""
        serializer.save(owner=self.request.user)

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


class LessonDestroy(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerUser]
