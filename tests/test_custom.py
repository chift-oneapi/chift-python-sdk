import datetime
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


def test_create_update_contact(custom_regate_consumer: Consumer):
    consumer = custom_regate_consumer

    data = {
        "external_id": None,
        "name": "testyyy fou",
        "customer_type": "company",
        "customer_reference": None,
        "payment_method": "bank_transfer",
        "balance_cents": 0,
        "yearly_billed_cents": 0,
        "discount_condition": "No discount granted for early payment.",
        "late_payment_penalties": "In the event of non-payment on the due date, penalties calculated at three times the legal interest rate will be applied.",
        "legal_fixed_compensation": "Any late payment will result in a fixed compensation for recovery costs of €40.",
        "company_number": None,
        "unit_number": None,
        "vat_number": None,
        "is_archived": None,
        "vat_exemption_reason": None,
        "address": {
            "id": "24819b3f-cd0a-43d9-9daa-d83a7d9b1985",
            "city": "test",
            "address_line_1": "test",
            "address_line_2": "test",
            "postal_code": "test",
            "country_code": "AF",
            "country": {"id": 4, "iso_alpha2": "AF", "name": "Afghanistan"},
        },
        "bank_accounts": [{"id": "4c108f34-1b95-45cf-a94b-b869675dc962"}],
    }

    contact = consumer.custom.Custom.create("regate", "contacts", data)

    assert contact

    data = {"legal_fixed_compensation": "12345"}
    contact = consumer.custom.Custom.update("regate", "contacts", contact["id"], data)

    assert contact["legal_fixed_compensation"] == "12345"


def test_create_product(custom_regate_consumer: Consumer):
    consumer = custom_regate_consumer

    data = {
        "sales_vat_account_id": "ee37ef01-725b-4bd6-a096-06d8093f2c82",
        "reference": str(uuid.uuid4()),
        "price_cents": 1000,
        "description": "A toothbrush is an oral hygiene tool used to clean the teeth, gums, and tongue. It consists of a head of tightly clustered bristles, atop of which toothpaste can be applied, mounted on a handle which facilitates the cleaning of hard-to-reach areas of the mouth.",
        "name": str(uuid.uuid4()),
        "price_currency": 100,
    }

    product = consumer.custom.Custom.create("regate", "products", data)

    assert product


def test_create_invoice(custom_regate_consumer: Consumer):
    consumer = custom_regate_consumer

    products = consumer.custom.Custom.all("regate", "products", limit=2)
    product_id = products[0].get("id")

    data = {
        "currency": "EUR",
        "payment_method": "bank_transfer",
        "urgent": False,
        "vat_paid": "receipts",
        "customer_id": "16b9969d-5d89-4fc5-8a84-46d7dcd89f4d",
        "delivery_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "due_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "lines": [
            {
                "quantity": 1,
                "unit_price_cents": 100,
                "sales_vat_account_id": "afe5673b-d379-4b6b-a2d5-187533497f78",
                "product_id": product_id,
            }
        ],
        "paid_amount_cents": 100,
    }

    invoice = consumer.custom.Custom.create("regate", "invoices", data)

    assert invoice
