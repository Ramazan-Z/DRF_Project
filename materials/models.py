from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):

    name: models.Field = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description: models.Field = models.TextField(
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    preview: models.Field = models.ImageField(
        blank=True,
        null=True,
        upload_to="materials/previews/",
        verbose_name="Превью курса",
        help_text="Загрузите превью курса",
    )
    owner: models.Field = models.ForeignKey(
        AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        related_name="user_courses",
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = "courses"
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):

    name: models.Field = models.CharField(
        max_length=255,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description: models.Field = models.TextField(
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )
    preview: models.Field = models.ImageField(
        blank=True,
        null=True,
        upload_to="materials/previews/",
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
    )
    video_link: models.Field = models.URLField(
        max_length=500,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )
    course: models.Field = models.ForeignKey(
        Course,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс",
        related_name="course_lessons",
    )
    owner: models.Field = models.ForeignKey(
        AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        related_name="user_lessons",
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = "lessons"
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name"]
