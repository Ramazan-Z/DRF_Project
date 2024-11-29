from django.contrib import admin

from materials.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):

    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ("course", "user")
    search_fields = ("course", "user")
