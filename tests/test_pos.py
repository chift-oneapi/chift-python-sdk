import pytest

from chift.openapi.models import Consumer
from tests.fixtures import pos


@pytest.mark.mock_chift_response(pos.CUSTOMER_CREATE, pos.CUSTOMER_GET)
def test_contact(pos_consumer: Consumer):
    consumer = pos_consumer

    # create contact
    data = {
        "first_name": "Test",
        "last_name": "Customer",
        "email": "test.customer@example.com",
    }
    expected_contact = consumer.pos.Customer.create(data)

    assert expected_contact.id, "create() failed"

    # find it back with its id
    actual_contact = consumer.pos.Customer.get(str(expected_contact.id))

    assert expected_contact == actual_contact, "get() failed"


@pytest.mark.mock_chift_response(
    pos.CUSTOMER_ALL, pos.CUSTOMER_ALL["items"][0], pos.CUSTOMER_ALL["items"][1]
)
def test_contact_all(pos_consumer: Consumer):
    consumer = pos_consumer
    contacts = consumer.pos.Customer.all(limit=2)

    assert contacts

    for contact in contacts:
        assert contact.first_name


@pytest.mark.mock_chift_response(
    pos.PAYMENT_METHOD_ALL,
    pos.PAYMENT_METHOD_ALL["items"][0],
    pos.PAYMENT_METHOD_ALL["items"][1],
)
def test_payment_methods_all(pos_consumer: Consumer):
    consumer = pos_consumer
    payments = consumer.pos.PaymentMethod.all(limit=2)

    assert payments

    for payment in payments:
        assert payment.name


@pytest.mark.mock_chift_response(
    pos.SALES_ITEM,
)
@pytest.mark.skip(
    reason="consumer.pos.Sale.all returning array but in API we have one item. Potential bug"
)
def test_sales_all(pos_consumer: Consumer):
    consumer = pos_consumer
    sales = consumer.pos.Sale.all(
        params={"date_from": "2023-01-08", "date_to": "2023-01-01"}, limit=2
    )
    assert sales


@pytest.mark.mock_chift_response(pos.PAYMENT_ALL)
def test_payment(pos_consumer: Consumer):
    consumer = pos_consumer
    payments = consumer.pos.Payment.all(
        params={"date_from": "2023-01-08", "date_to": "2023-01-01"}, limit=2
    )

    for payment in payments:
        assert payment.payment_method_name


@pytest.mark.mock_chift_response(
    pos.LOCATION_ALL, pos.LOCATION_ALL["items"][0], pos.LOCATION_ALL["items"][1]
)
def test_location(pos_consumer: Consumer):
    consumer = pos_consumer

    locations = consumer.pos.Location.all(limit=2)

    assert locations

    for location in locations:
        assert location.id


@pytest.mark.mock_chift_response(
    pos.ORDER_ALL, pos.ORDER_ALL["items"][0], pos.ORDER_ALL["items"][1]
)
def test_order(pos_consumer: Consumer):
    consumer = pos_consumer

    orders = consumer.pos.Order.all(
        {"date_from": "2023-01-08", "date_to": "2023-01-01"}
    )

    for order in orders:  # probably no order in given timeframe
        assert order == consumer.pos.Order.get(order.id)


@pytest.mark.mock_chift_response(pos.CLOSURE)
def test_closure(pos_consumer: Consumer):
    consumer = pos_consumer

    closure = consumer.pos.Closure.get("2023-01-01")

    assert closure.status


@pytest.mark.mock_chift_response(
    pos.PRODUCT_ALL,
    pos.PRODUCT_ALL["items"][0],
)
def test_product_all(pos_consumer: Consumer):
    consumer = pos_consumer

    products = consumer.pos.Product.all(limit=1)

    assert products
    for product in products:
        assert product.name


@pytest.mark.mock_chift_response(
    pos.PRODUCT_CATEGORY_ALL,
    pos.PRODUCT_CATEGORY_ALL["items"][0],
)
def test_productcategories_all(pos_consumer: Consumer):
    consumer = pos_consumer
    categories = consumer.pos.ProductCategory.all()

    assert categories
    for category in categories:
        assert category.id
