from django.urls import path
from rest_framework import routers

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")

urlpatterns = [
    path("pyments/", views.PymentsList.as_view(), name="pyments-list"),
] + router.urls
