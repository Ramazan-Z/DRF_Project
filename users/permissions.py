from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class ProfilePermissionsClass(BasePermission):
    """Права доступа на редактирование и удаление профиля"""

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        return bool(obj == request.user)
