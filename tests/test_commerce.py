from chift.openapi.models import Consumer


def test_contact(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer

    contacts = consumer.commerce.Customer.all(limit=2)

    assert contacts

    for contact in contacts:
        expected_contact = consumer.commerce.Customer.get(contact.id)
        assert contact == expected_contact


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


def test_location(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer

    locations = consumer.commerce.Location.all(limit=2)

    assert locations


def test_order(ecommerce_consumer: Consumer):
    consumer = ecommerce_consumer
    # TODO: test create()

    orders = consumer.commerce.Order.all(limit=2)

    assert orders

    for order in orders:
        expected_order = consumer.commerce.Order.get(order.id)
        assert order.id == expected_order.id
