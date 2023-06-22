import datetime
import uuid

import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


def test_contact(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

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

    # find it back in all
    found_contact = None
    contacts = consumer.invoicing.Contact.all()
    for actual_contact in contacts:
        if expected_contact == actual_contact:
            found_contact = actual_contact
            break

    assert found_contact == actual_contact, "all() failed"

    # find it back with its id
    actual_contact = consumer.invoicing.Contact.get(str(expected_contact.id))

    assert expected_contact == actual_contact, "get() failed"


def test_invoice(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

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

    # find it back in all
    found_invoice = None
    invoices = consumer.invoicing.Invoice.all({"invoice_type": "customer_invoice"})
    for actual_invoice in invoices:
        if expected_invoice == actual_invoice:
            found_invoice = actual_invoice
            break

    assert found_invoice == actual_invoice, "all() failed"

    # find it back with its id
    actual_invoice = consumer.invoicing.Invoice.get(str(expected_invoice.id))

    assert expected_invoice == actual_invoice, "get() failed"


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

    # find it back in all
    found_product = None
    products = consumer.invoicing.Product.all()
    for actual_product in products:
        if expected_product == actual_product:
            found_product = actual_product
            break

    assert found_product == actual_product, "all() failed"

    # find it back with its id
    actual_product = consumer.invoicing.Product.get(str(expected_product.id))

    assert expected_product == actual_product, "get() failed"


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
