from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsModeratorUser(BasePermission):
    """Определение прав модератора"""

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        return bool(user.groups.filter(name="Moderators").exists() or user.is_superuser)


class IsOwnerUser(BasePermission):
    """Определение прав владельца"""

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        return bool(request.user == obj.owner)
