from django.urls import path
from rest_framework import routers

from materials import views
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = routers.DefaultRouter()
router.register(r"courses", views.CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", views.LessonList.as_view(), name="lessons-list"),
    path("lessons/<int:pk>/", views.LessonRetrieve.as_view(), name="lessons-retrieve"),
    path("lessons/create/", views.LessonCreate.as_view(), name="lessons-create"),
    path("lessons/<int:pk>/update/", views.LessonUpdate.as_view(), name="lessons-update"),
    path("lessons/<int:pk>/delete/", views.LessonDestroy.as_view(), name="lessons-delete"),
] + router.urls
