from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import BaseSerializer

from users import serializers
from users.models import Pyment, User
from users.permissions import ProfilePermissionsClass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self) -> Any:
        """Права доступа в зависимости от действия"""
        if self.action == "create":
            self.permission_classes = [AllowAny]
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = [IsAuthenticated, ProfilePermissionsClass]
        return super().get_permissions()

    def get_serializer_class(self) -> Any:
        """Сериализатор в зависимости от действия"""
        if self.action == "list":
            return serializers.UserSerializer
        if self.action in ("create", "update", "partial_update"):
            return serializers.UserRegisterSerializer
        if self.get_object() == self.request.user:
            return serializers.UserSelfSerializer
        return serializers.UserSerializer

    def perform_create(self, serializer: BaseSerializer) -> Any:
        """Регистрация пользователя"""
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class PaymentsList(generics.ListAPIView):
    serializer_class = serializers.PaymentSerializer

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ("created_at",)
    filterset_fields = ("course", "lesson", "pyment_method")

    def get_queryset(self) -> Any:
        """Фильтрация чужих платежей из списка"""
        user = self.request.user
        if user.groups.filter(name="Moderators").exists() or user.is_superuser:
            return Pyment.objects.all()
        return Pyment.objects.filter(user=user)
