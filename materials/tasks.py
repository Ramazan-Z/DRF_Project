from typing import Any

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription


@shared_task
def notify_users(data: dict[str:Any]) -> None:
    subject = "Уведомление об изменениях на курсе"
    message = f"Материалы курса <{data['name']}> обновились. Заходите посмотреть"
    from_email = EMAIL_HOST_USER
    subscriptions = Subscription.objects.filter(course=data["id"])
    recipient_list = [subscription.user.email for subscription in list(subscriptions)]
    send_mail(subject, message, from_email, recipient_list)
