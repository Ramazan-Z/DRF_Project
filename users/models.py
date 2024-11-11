from django.contrib.auth.models import AbstractUser
from django.db import models


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
