from chift.openapi.models import Consumer


def test_transactions(payment_consumer: Consumer):
    consumer = payment_consumer

    transactions = consumer.payment.Transaction.all(limit=2)

    assert transactions

    for transaction in transactions:
        assert transaction.id


def test_balances(payment_consumer: Consumer):
    consumer = payment_consumer

    balances = consumer.payment.Balance.all(limit=2)

    assert balances

    for balance in balances:
        assert balance.id
