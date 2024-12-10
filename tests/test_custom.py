import uuid

from chift.openapi.models import Consumer


def test_get_products(custom_regate_consumer: Consumer):
    consumer = custom_regate_consumer

    products = consumer.custom.Custom.all("regate", "products", limit=2)

    assert products and len(products) <= 2


def test_get_contacts(custom_regate_consumer: Consumer):
    consumer = custom_regate_consumer

    contacts = consumer.custom.Custom.all("regate", "contacts", limit=2)

    assert contacts and len(contacts) <= 2


def test_create_product(custom_regate_consumer: Consumer):
    consumer = custom_regate_consumer

    data = {
        "sales_vat_account_id": "ee37ef01-725b-4bd6-a096-06d8093f2c82",
        "reference": str(uuid.uuid4()),
        "price_cents": 1000,
        "description": "A toothbrush is an oral hygiene tool used to clean the teeth, gums, and tongue. It consists of a head of tightly clustered bristles, atop of which toothpaste can be applied, mounted on a handle which facilitates the cleaning of hard-to-reach areas of the mouth.",
        "name": str(uuid.uuid4()),
        "price_currency": "EUR",
    }

    product = consumer.custom.Custom.create("regate", "products", data)

    assert product
