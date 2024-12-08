from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users import serializers, services
from users.models import Pyment, User
from users.permissions import ProfilePermissionsClass


class CustomTokenObtainPairView(TokenObtainPairView):
    """Контроллер получения токена авторизации"""

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Переопределение метода для установки даты последнего входа"""
        response = super().post(request, *args, **kwargs)
        user = get_object_or_404(User, email=request.data.get("email"))
        user.last_login = timezone.now()
        user.save()
        return response


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
        if self.kwargs.get("pk") == self.request.user.pk:
            return serializers.UserSelfSerializer
        return serializers.UserSerializer

    def perform_create(self, serializer: BaseSerializer) -> Any:
        """Регистрация пользователя"""
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class PaymentsList(generics.ListAPIView):
    queryset = Pyment.objects.all()
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


class PaymentCreateView(generics.CreateAPIView):
    queryset = Pyment.objects.all()
    serializer_class = serializers.PaymentCreateSerializer

    def perform_create(self, serializer: BaseSerializer) -> Any:
        """Создание объекта платежа"""
        payment = serializer.save(user=self.request.user, pyment_method="transfer")
        product = services.get_or_create_product(payment)
        price = services.create_price(product, payment.amount)
        session = services.create_session(price, payment.user, self.request._current_scheme_host)
        payment.session_id = session.id
        payment.payment_url = session.url
        payment.save()


def success_pay(request: HttpRequest) -> HttpResponse:
    """Контроллер страницы успешной оплаты"""
    return HttpResponse("Спасибо, Ваш платеж успешно выполнен")
