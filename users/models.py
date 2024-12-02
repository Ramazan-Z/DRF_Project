from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Укажите эл. почту",
    )
    phone_number: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=15,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    sity: models.Field = models.CharField(
        blank=True,
        null=True,
        max_length=60,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar: models.Field = models.ImageField(
        blank=True,
        null=True,
        upload_to="users/avatars/",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return str(self.username)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Pyment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("cach", "Наличными"),
        ("transfer", "Перевод на счет"),
    ]

    user: models.Field = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        related_name="pyments_user",
    )
    created_at: models.Field = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата платежа",
    )
    course: models.Field = models.ForeignKey(
        Course,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        help_text="Укажите курс для оплаты",
        related_name="pyments_course",
    )
    lesson: models.Field = models.ForeignKey(
        Lesson,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        help_text="Укажите урок для оплаты",
        related_name="pyments_lesson",
    )
    amount: models.Field = models.PositiveIntegerField(
        verbose_name="Сумма платежа",
        help_text="Укажите сумму платежа",
    )
    pyment_method: models.Field = models.CharField(
        max_length=8,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        default="cach",
        verbose_name="Способ платежа",
        help_text="Укажите способ платежа",
    )
    session_id: models.Field = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Идентификатор платежа",
    )
    payment_url: models.Field = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на платеж",
    )

    def __str__(self) -> str:
        return f"{self.created_at}: {self.course if self.course else self.lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["created_at"]
