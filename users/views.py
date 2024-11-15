from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter

from users import serializers
from users.models import Pyment, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PymentsList(generics.ListAPIView):
    queryset = Pyment.objects.all()
    serializer_class = serializers.PymentSerializer

    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ("created_at",)
    filterset_fields = ("course", "lesson", "pyment_method")
