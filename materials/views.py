from rest_framework import generics, viewsets

from materials import serializers
from materials.models import Course, Lesson


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer


class LessonList(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer


class LessonRetrieve(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer


class LessonCreate(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer


class LessonUpdate(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer


class LessonDestroy(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
