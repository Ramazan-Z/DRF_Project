from typing import Any

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import VideoLinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoLinkValidator(field="video_link")]


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="course_lessons")

    @staticmethod
    def get_lessons_count(course: Course) -> Any:
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"
