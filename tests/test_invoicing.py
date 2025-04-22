import pytest

from chift.openapi.models import Consumer
from tests.fixtures import invoicing


@pytest.mark.mock_chift_response(invoicing.CONTACT_CREATE, invoicing.CONTACT_GET)
def test_contact(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    # create contact
    data = {
        "first_name": "Test",
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


@pytest.mark.mock_chift_response(
    invoicing.CONTACT_ALL,
    invoicing.CONTACT_ALL["items"][0],
    invoicing.CONTACT_ALL["items"][1],
)
def test_contacts(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    contacts = consumer.invoicing.Contact.all(limit=2)

    assert contacts

    for contact in contacts:
        assert contact.id
        assert contact.source_ref


@pytest.mark.mock_chift_response(
    invoicing.CONTACT_CREATE, invoicing.INVOICE_CREATE, invoicing.INVOICE_GET
)
def test_invoice(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    # first create a contact to use in the invoice
    contact_data = {
        "first_name": "Test",
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
    contact = consumer.invoicing.Contact.create(contact_data)

    # create invoice
    invoice_data = {
        "invoice_type": "customer_invoice",
        "invoice_number": invoicing.INVOICE_CREATE["invoice_number"],
        "partner_id": str(contact.id),
        "status": "draft",
        "currency": "EUR",
        "invoice_date": invoicing.INVOICE_CREATE["invoice_date"],
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

    expected_invoice = consumer.invoicing.Invoice.create(invoice_data)

    assert expected_invoice.partner_id == contact.id, "create() failed"
    assert expected_invoice.invoice_type.value == "customer_invoice", "create() failed"

    # find it back with its id
    actual_invoice = consumer.invoicing.Invoice.get(str(expected_invoice.id))

    assert expected_invoice == actual_invoice, "get() failed"


@pytest.mark.mock_chift_response(
    invoicing.INVOICE_ALL,
    invoicing.INVOICE_ALL["items"][0],
    invoicing.INVOICE_ALL["items"][1],
)
def test_invoices(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    invoices = consumer.invoicing.Invoice.all(
        {"invoice_type": "customer_invoice"}, limit=2
    )

    assert invoices
    assert len(invoices) == 2

    for invoice in invoices:
        assert invoice.id
        assert invoice.invoice_number
        assert len(invoice.lines) > 0


@pytest.mark.mock_chift_response(invoicing.PRODUCT_CREATE, invoicing.PRODUCT_GET)
def test_product(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    # create product
    data = {
        "code": invoicing.PRODUCT_CREATE["code"],
        "name": invoicing.PRODUCT_CREATE["name"],
        "unit": "U",
        "unit_price": 100,
    }

    expected_product = consumer.invoicing.Product.create(data)

    assert expected_product.id, "create() failed"

    # find it back with its id
    actual_product = consumer.invoicing.Product.get(str(expected_product.id))

    assert expected_product.id == actual_product.id, "get() failed"
    assert expected_product.name == actual_product.name, "get() failed"


@pytest.mark.mock_chift_response(
    invoicing.PRODUCT_ALL,
    invoicing.PRODUCT_ALL["items"][0],
    invoicing.PRODUCT_ALL["items"][1],
)
def test_products(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    products = consumer.invoicing.Product.all(limit=2)

    assert products
    assert len(products) == 2

    for product in products:
        assert product.id
        assert product.name


@pytest.mark.mock_chift_response(invoicing.TAX_ALL, invoicing.TAX_GET)
def test_tax(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    taxes = consumer.invoicing.Tax.all()
    assert taxes
    assert len(taxes) == 3

    expected_tax = taxes[0]
    actual_tax = consumer.invoicing.Tax.get(expected_tax.id)

    assert expected_tax == actual_tax, "get() failed"
    assert actual_tax.label == "VAT 21%"
    assert actual_tax.rate == 21.0


@pytest.mark.mock_chift_response(invoicing.PAYMENT_METHOD_ALL)
def test_payment_methods(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    payment_methods = consumer.invoicing.PaymentMethod.all()

    assert payment_methods
    assert len(payment_methods) == 2

    for method in payment_methods:
        assert method.id
        assert method.name


@pytest.mark.mock_chift_response(invoicing.PAYMENT_ALL)
def test_payments(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    payments = consumer.invoicing.Payment.all()

    assert payments
    assert len(payments) == 2

    for payment in payments:
        assert payment.id
        assert payment.amount
        assert payment.currency
        assert payment.status


@pytest.mark.mock_chift_response(invoicing.CUSTOM_CASHES, invoicing.CUSTOM_CASH_ENTRIES)
def test_custom(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

    cashes = consumer.invoicing.Custom.all("cashes")
    assert cashes
    assert len(cashes) == 2

    # Test getting entries for the first cash register
    cash_id = cashes[0]["cashid"]
    entries = consumer.invoicing.Custom.all(f"cashes/{cash_id}/entries")

    assert entries
    assert len(entries) == 2

    # Create operation would fail as shown in the original test
    # with pytest.raises(Exception) as e:
    #     consumer.invoicing.Custom.create(
    #         f"cashes/{cash_id}/entries",
    #         {
    #             "amount": 100,
    #             "description": "Test entry"
    #         }
    #     )
    #
    # assert "was not created" in str(e.value)
