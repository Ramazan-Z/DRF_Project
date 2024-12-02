from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register("", views.UserViewSet, basename="users")

urlpatterns = [
    path("payments/", views.PaymentsList.as_view(), name="pyments-list"),
    path("payments/create/", views.PaymentCreateView.as_view(), name="payment-create"),
    path("success_pay/", views.success_pay, name="success-pay"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
