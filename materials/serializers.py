from typing import Any

from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import VideoLinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoLinkValidator(field="video_link")]


class CourseSerializer(ModelSerializer):
    subscribed = SerializerMethodField()
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="course_lessons")

    @staticmethod
    def get_lessons_count(course: Course) -> Any:
        return Lesson.objects.filter(course=course).count()

    def get_subscribed(self, course: Course) -> Any:
        request = self.context.get("request")
        user = request.user if request else None
        return Subscription.objects.filter(course=course, user=user).exists()

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class Subscribe(Serializer):
    """Сообщение о создании/удалении подписки"""

    message = CharField(max_length=50)
