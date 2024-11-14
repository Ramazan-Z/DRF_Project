from rest_framework import routers

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register("", views.UserViewSet, basename="users")

urlpatterns = router.urls
