import random

from chift.openapi.models import Consumer


def test_transactions(payment_consumer: Consumer):
    consumer = payment_consumer

    transactions = consumer.payment.Transaction.all(limit=2)

    # unfortunatly, there is no transaction in our accounts
    # assert transactions

    for transaction in transactions:
        assert transaction.id


def test_balances(payment_consumer: Consumer):
    consumer = payment_consumer

    balances = consumer.payment.Balance.all(limit=2)

    assert balances

    for balance in balances:
        assert balance.id


def test_payments(payment_consumer: Consumer):
    consumer = payment_consumer

    payments = consumer.payment.Payment.all(limit=2)

    assert payments

    for payment in payments:
        assert payment.id

    payment_id = random.choice(payments).id
    payment = consumer.payment.Payment.get(payment_id)
    assert payment
    assert payment.id
