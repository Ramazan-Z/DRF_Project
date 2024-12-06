from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription
from users.models import User


@shared_task
def notify_users(course_id: int, course_name: str) -> None:
    """Уведомление пользователей об изменениях на курсе"""
    subject = "Уведомление об изменениях на курсе"
    message = f"Материалы курса <{course_name}> обновились. Заходите посмотреть"
    from_email = EMAIL_HOST_USER
    subscriptions = Subscription.objects.filter(course=course_id)
    recipient_list = [subscription.user.email for subscription in list(subscriptions)]
    if recipient_list:
        send_mail(subject, message, from_email, recipient_list)


@shared_task
def block_user() -> None:
    """Блокировка пользователей, "пропавших" на месяц"""
    users = User.objects.all()
    today = timezone.now()
    for user in list(users):
        if not user.last_login:
            user.last_login = today
            user.save()
        if (today - user.last_login) > timedelta(days=30) and not user.is_superuser and user.is_active:
            user.is_active = False
            user.save()
