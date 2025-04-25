import pytest

from chift.openapi.models import Consumer
from tests.fixtures import ecommerce


@pytest.mark.mock_chift_response(
    ecommerce.CUSTOMER_ALL,
    ecommerce.CUSTOMER_ALL["items"][0],
    ecommerce.CUSTOMER_ALL["items"][1],
)
def test_contact(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer

    contacts = consumer.commerce.Customer.all(limit=2)

    assert contacts

    for contact in contacts:
        expected_contact = consumer.commerce.Customer.get(contact.id)
        assert contact == expected_contact


@pytest.mark.mock_chift_response(
    ecommerce.PRODUCT_ALL,
    ecommerce.PRODUCT_ALL["items"][0],
    ecommerce.PRODUCT_ALL["items"][0]["variants"][0],
    ecommerce.PRODUCT_ALL["items"][1],
    ecommerce.PRODUCT_ALL["items"][1]["variants"][0],
)
def test_product(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer

    products = consumer.commerce.Product.all(limit=2)

    assert products

    for product in products:
        expected_product = consumer.commerce.Product.get(product.id)
        assert product.id == expected_product.id

        # test_variant
        for variant_expected in product.variants:
            variant = consumer.commerce.Variant.get(variant_expected.id)
            assert variant.id == variant_expected.id
            assert variant.available_quantity == variant_expected.available_quantity


@pytest.mark.mock_chift_response(
    ecommerce.LOCATION_ALL,
)
def test_location(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer

    locations = consumer.commerce.Location.all(limit=2)

    assert locations


@pytest.mark.mock_chift_response(
    ecommerce.PAYMENT_METHOD_ALL,
)
def test_payment_method(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer

    payment_methods = consumer.commerce.PaymentMethod.all(limit=2)

    assert payment_methods


@pytest.mark.mock_chift_response(
    ecommerce.PRODUCT_CATEGORY_ALL,
)
def test_product_categories(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer

    product_categories = consumer.commerce.ProductCategory.all(limit=2)

    assert product_categories


@pytest.mark.mock_chift_response(
    ecommerce.TAX_ALL,
)
def test_taxes(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer

    taxes = consumer.commerce.Tax.all(limit=2)
    assert taxes


@pytest.mark.mock_chift_response(
    ecommerce.ORDER_ALL,
    ecommerce.ORDER_ALL["items"][0],
    ecommerce.ORDER_ALL["items"][1],
)
def test_order(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer
    # TODO: test create()

    orders = consumer.commerce.Order.all(limit=2)

    assert orders

    for order in orders:
        expected_order = consumer.commerce.Order.get(order.id)
        assert order.id == expected_order.id
