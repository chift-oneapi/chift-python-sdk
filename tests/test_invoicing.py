import datetime
import uuid

import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


def test_contact(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    # create contact
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
    expected_contact = consumer.invoicing.Contact.create(data)

    assert expected_contact.id, "create() failed"

    # find it back with its id
    actual_contact = consumer.invoicing.Contact.get(str(expected_contact.id))

    assert expected_contact == actual_contact, "get() failed"


def test_contacts(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    contacts = consumer.invoicing.Contact.all(limit=2)

    assert contacts

    for contact in contacts:
        assert contact.id


def test_invoice(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    # find contact required in invoice
    contact = consumer.invoicing.Contact.all(
        limit=1, params={"contact_type": "customer"}
    )[0]

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


def test_invoices(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    invoices = consumer.invoicing.Invoice.all(
        {"invoice_type": "customer_invoice"}, limit=2
    )

    assert invoices

    for invoice in invoices:
        assert invoice.id


def test_product(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

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

    assert expected_product == actual_product, "get() failed"


def test_products(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    products = consumer.invoicing.Product.all(limit=2)

    assert products

    for product in products:
        assert product.id


def test_tax(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    taxes = consumer.invoicing.Tax.all()

    expected_tax = taxes[0]

    actual_tax = consumer.invoicing.Tax.get(expected_tax.id)

    assert expected_tax == actual_tax, "get() failed"


def test_opportunity(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    with pytest.raises(ChiftException) as e:
        consumer.invoicing.Opportunity.all()

    assert e.value.message == "API Resource does not exist"
