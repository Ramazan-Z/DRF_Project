import os

import stripe
from django.urls import reverse

from users.models import Pyment, User

stripe.api_key = os.getenv("STRIPE_API_KEY")


def get_or_create_product(payment: Pyment) -> stripe.Product:
    """Получение или создание продукта"""
    if payment.course:
        paid_product = payment.course
        product_id = f"course_{paid_product.pk}"
    else:
        paid_product = payment.lesson
        product_id = f"lesson_{paid_product.pk}"

    try:
        product = stripe.Product.retrieve(product_id)
    except stripe._error.InvalidRequestError:
        product = stripe.Product.create(
            id=product_id,
            name=paid_product.name,
            description=paid_product.description,
        )

    return product


def create_price(product: stripe.Product, amount: int) -> stripe.Price:
    """Создание объекта цены"""
    price = stripe.Price.create(currency="rub", unit_amount=amount * 100, product=product.id)
    return price


def create_session(price: stripe.Price, user: User, scheme: str) -> stripe.checkout.Session:
    """Создание сессии оплаты"""
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": price.id, "quantity": 1}],
        customer_email=user.email,
        success_url=f"{scheme}{reverse('users:success-pay')}",
    )
    return session


def get_session_status(payment: Pyment) -> str:
    """Получение статуса платежа"""
    try:
        session = stripe.checkout.Session.retrieve(str(payment.session_id))
    except stripe._error.InvalidRequestError:
        return "unknown"
    return str(session.status)
