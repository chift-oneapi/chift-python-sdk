import datetime
import uuid

import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


def create_contact(consumer: Consumer):
    name = str(uuid.uuid1())
    data = {
        "first_name": name,
        "addresses": [
            {
                "address_type": "main",
                "street": "street",
                "city": "city",
                "postal_code": "postal_code",
                "country": "BE",
            }
        ],
    }
    return consumer.invoicing.Contact.create(data)


def test_contact(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    expected_contact = create_contact(consumer)

    assert expected_contact.id, "create() failed"

    # find it back with its id
    actual_contact = consumer.invoicing.Contact.get(str(expected_contact.id))

    assert expected_contact == actual_contact, "get() failed"


def test_contacts(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    contacts = consumer.invoicing.Contact.all(limit=2)

    assert contacts

    for contact in contacts:
        assert contact.id


def test_invoice(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    # find contact required in invoice
    contact = create_contact(consumer)

    # create invoice
    data = {
        "invoice_type": "customer_invoice",
        "invoice_number": str(uuid.uuid1()),
        "partner_id": str(contact.id),
        "status": "posted",
        "currency": "EUR",
        "invoice_date": datetime.date.today().strftime("%Y-%m-%d"),
        "tax_amount": 100,
        "untaxed_amount": 100,
        "total": 100,
        "lines": [
            {
                "product_code": "123",
                "description": "desc",
                "quantity": 1,
                "unit_price": 100,
                "tax_amount": 100,
                "total": 100,
                "untaxed_amount": 100,
                "tax_rate": 10.0,
            }
        ],
    }

    expected_invoice = consumer.invoicing.Invoice.create(data)

    assert expected_invoice.partner_id == contact.id, "create() failed"
    assert expected_invoice.invoice_type.value == "customer_invoice", "create() failed"

    # find it back with its id
    actual_invoice = consumer.invoicing.Invoice.get(str(expected_invoice.id))

    assert expected_invoice == actual_invoice, "get() failed"


def test_invoices(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    invoices = consumer.invoicing.Invoice.all(
        {"invoice_type": "customer_invoice"}, limit=2
    )

    assert invoices

    for invoice in invoices:
        assert invoice.id


def test_product(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    # create product
    data = {
        "code": str(uuid.uuid1())[:20],
        "name": str(uuid.uuid1()),
        "unit": "U",
        "unit_price": 100,
    }

    expected_product = consumer.invoicing.Product.create(data)

    assert expected_product.id, "create() failed"

    # find it back with its id
    actual_product = consumer.invoicing.Product.get(str(expected_product.id))

    assert expected_product.id == actual_product.id, "get() failed"
    assert expected_product.name == actual_product.name, "get() failed"


def test_products(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    products = consumer.invoicing.Product.all(limit=2)

    assert products

    for product in products:
        assert product.id


def test_tax(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    taxes = consumer.invoicing.Tax.all()

    expected_tax = taxes[0]

    actual_tax = consumer.invoicing.Tax.get(expected_tax.id)

    assert expected_tax == actual_tax, "get() failed"


def test_opportunity(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    with pytest.raises(ChiftException) as e:
        consumer.invoicing.Opportunity.all()

    assert e.value.message == "API Resource does not exist"


def test_custom(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    cashes = consumer.invoicing.Custom.all("cashes")
    assert cashes

    for cashe in cashes[:1]:  # 1 is enough
        entries = consumer.invoicing.Custom.all(f"cashes/{cashe.get('cashid')}/entries")
        assert entries

        with pytest.raises(ChiftException) as e:
            consumer.invoicing.Custom.create(
                f"cashes/{cashe.get('cashid')}/entries", {"ok": "ok"}
            )

        assert "was not created" in e.value.message
