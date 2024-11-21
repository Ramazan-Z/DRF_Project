from rest_framework.serializers import ModelSerializer

from users.models import Pyment, User


class PaymentSerializer(ModelSerializer):
    """Сериализатор просмотра платежей"""

    class Meta:
        model = Pyment
        fields = ("created_at", "course", "lesson", "amount", "pyment_method")


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
