from typing import Any

from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    """Валидатор ссылок на материалы урока"""

    def __init__(self, field: str) -> None:
        self.field = field

    def __call__(self, data: dict[str, Any]) -> None:
        if "youtube.com" not in data.get(self.field, ""):
            raise ValidationError("Допускаются только ссылки на видео youtube.com")
