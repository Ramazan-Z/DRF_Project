from typing import Any

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users import services
from users.models import Pyment, User
from users.validators import payment_amount_validator, payment_create_validator


class PaymentSerializer(ModelSerializer):
    """Сериализатор просмотра платежей"""

    status = SerializerMethodField()

    @staticmethod
    def get_status(payment: Pyment) -> Any:
        return services.get_session_status(payment)

    class Meta:
        model = Pyment
        fields = ("created_at", "course", "lesson", "amount", "pyment_method", "status", "payment_url")


class UserSerializer(ModelSerializer):
    """Сеарилизатор просмотра чужого профиля"""

    class Meta:
        model = User
        fields = ("id", "email", "username", "sity", "avatar")


class UserSelfSerializer(ModelSerializer):
    """Сеарилизатор просмотра своего профиля"""

    payments = PaymentSerializer(many=True, read_only=True, source="pyments_user")

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "sity",
            "avatar",
            "date_joined",
            "last_login",
            "payments",
        )


class UserRegisterSerializer(ModelSerializer):
    """Сериализатор регистрации/редактирования пользователя."""

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "phone_number", "sity", "avatar", "password")


class PaymentCreateSerializer(ModelSerializer):
    """Сериализатор создания платежa"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Pyment
        fields = "__all__"
        validators = [payment_create_validator, payment_amount_validator]
