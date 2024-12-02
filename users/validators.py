from typing import Any

from rest_framework.serializers import ValidationError


def payment_create_validator(data: dict[str, Any]) -> None:
    """Валидатор создания платежа"""
    if not (("course" in data) ^ ("lesson" in data)):
        raise ValidationError("Укажите только курс или только урок")


def payment_amount_validator(data: dict[str, Any]) -> None:
    """Валидатор суммы платежа"""
    if data["amount"] < 100:
        raise ValidationError("Минимальный платеж 100 руб.")
