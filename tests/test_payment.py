import random

import pytest

from chift.openapi.models import Consumer
from chift.openapi.openapi import TransactionItemOut
from tests.fixtures import payment


@pytest.mark.mock_chift_response(payment.TRANSACTIONS_ALL)
def test_transactions(payment_consumer: Consumer):
    consumer = payment_consumer

    transactions = consumer.payment.Transaction.all(limit=2)

    # unfortunatly, there is no transaction in our accounts
    # assert transactions

    for transaction in transactions:
        assert transaction.id


@pytest.mark.mock_chift_response(payment.BALANCES_ALL)
def test_balances(payment_consumer: Consumer):
    consumer = payment_consumer

    balances = consumer.payment.Balance.all(limit=2)

    assert balances

    for balance in balances:
        assert balance.id


@pytest.mark.mock_chift_response(payment.PAYMENTS_ALL, payment.PAYMENT_GET)
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


@pytest.mark.mock_chift_response(
    payment.REFUNDS_ALL,
    payment.PAYMENTS_ALL["items"][0],
    payment.PAYMENTS_ALL["items"][1],
)
def test_refunds(payment_consumer: Consumer):
    consumer = payment_consumer

    refunds = consumer.payment.Refund.all(limit=2)
    for refund in refunds:
        assert refund.id
        assert refund.payment_id
        payment = consumer.payment.Payment.get(refund.payment_id)
        assert payment
        assert payment.id


@pytest.mark.parametrize(
    "category", ["internal_move", "internal_move_out", "internal_move_in"]
)
def test_a_transaction_accepts_every_internal_move_category(category: str):
    item = {**payment.TRANSACTIONS_ALL["items"][0], "accounting_category": category}

    assert TransactionItemOut.model_validate(item).accounting_category.value == category
