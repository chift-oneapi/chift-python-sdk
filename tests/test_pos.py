import uuid

import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


def test_contact(zelty_consumer: Consumer):
    consumer = zelty_consumer

    # create contact
    data = {
        "first_name": str(uuid.uuid1()),
        "last_name": str(uuid.uuid1()),
        "email": f"{str(uuid.uuid1())}@test.com",
    }
    expected_contact = consumer.pos.Customer.create(data)

    assert expected_contact.id, "create() failed"

    # find it back with its id
    actual_contact = consumer.pos.Customer.get(str(expected_contact.id))

    assert expected_contact == actual_contact, "get() failed"


def test_contact_all(zelty_consumer: Consumer):
    consumer = zelty_consumer
    contacts = consumer.pos.Customer.all(limit=2)

    assert contacts

    for contact in contacts:
        assert contact.first_name


def test_payment_methods_all(zelty_consumer: Consumer):
    consumer = zelty_consumer
    payments = consumer.pos.PaymentMethod.all(limit=2)

    assert payments

    for payment in payments:
        assert payment.name


def test_sales_all(zelty_consumer: Consumer):
    consumer = zelty_consumer
    sales = consumer.pos.Sale.all(
        params={"date_from": "2023-01-08", "date_to": "2023-01-01"}, limit=2
    )

    for sale in sales:  # probably no sale in given timeframe
        assert sale.total


def test_payment(zelty_consumer: Consumer):
    consumer = zelty_consumer

    with pytest.raises(ChiftException) as e:
        consumer.pos.Payment.all(
            params={"date_from": "2023-01-08", "date_to": "2023-01-01"}, limit=2
        )

    assert e.value.message == "API Resource does not exist"


def test_location(zelty_consumer: Consumer):
    consumer = zelty_consumer

    locations = consumer.pos.Location.all(limit=2)

    assert locations

    for location in locations:
        assert location.id


def test_order(zelty_consumer: Consumer):
    consumer = zelty_consumer

    orders = consumer.pos.Order.all(
        {"date_from": "2023-01-08", "date_to": "2023-01-01"}
    )

    for order in orders:  # probably no order in given timeframe
        assert order == consumer.pos.Order.get(order.id)


def test_closure(zelty_consumer: Consumer):
    consumer = zelty_consumer

    closure = consumer.pos.Closure.get("2023-01-01")

    assert closure.status
