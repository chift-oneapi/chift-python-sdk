from chift.openapi.models import Consumer


def test_analytic_plan(odoo_consumer: Consumer):
    consumer = odoo_consumer

    plans = consumer.accounting.AnalyticPlan.all(limit=2)

    assert plans

    for plan in plans:
        assert plan.id


def test_tax(odoo_consumer: Consumer):
    consumer = odoo_consumer

    taxes = consumer.accounting.Tax.all(limit=2)

    assert taxes

    for tax in taxes:
        assert tax.id


def test_account(odoo_consumer: Consumer):
    consumer = odoo_consumer

    accounts = consumer.accounting.Account.all(limit=2)

    assert accounts

    for account in accounts:
        assert account.number


def test_operation(odoo_consumer: Consumer):
    consumer = odoo_consumer

    operations = consumer.accounting.MiscellaneousOperation.all(limit=2)

    assert operations

    for operation in operations:
        expected_operation = consumer.accounting.MiscellaneousOperation.get(
            operation.id
        )

        assert operation == expected_operation


def test_client(odoo_consumer: Consumer):
    consumer = odoo_consumer

    clients = consumer.accounting.Client.all(limit=2)

    assert clients

    for client in clients:
        expected_client = consumer.accounting.Client.get(client.id)

        assert client == expected_client


def test_update_client(odoo_consumer: Consumer):
    consumer = odoo_consumer

    clients = consumer.accounting.Client.all(limit=2)

    assert clients

    for client in clients:
        current_website = client.website

        updated_client = consumer.accounting.Client.update(client.id, {'website': 'https://test.com'})
        assert updated_client.website == 'https://test.com'

        consumer.accounting.Client.update(client.id, {'website': current_website}) # revert
        break # one is enough


def test_supplier(odoo_consumer: Consumer):
    consumer = odoo_consumer

    suppliers = consumer.accounting.Supplier.all(limit=2)

    assert suppliers

    for supplier in suppliers:
        expected_supplier = consumer.accounting.Supplier.get(supplier.id)

        assert supplier == expected_supplier


def test_invoice(odoo_consumer: Consumer):
    consumer = odoo_consumer

    invoices = consumer.accounting.Invoice.all("customer_invoice", limit=2)

    assert invoices

    for invoice in invoices:
        expected_invoice = consumer.accounting.Invoice.get(invoice.id)

        assert invoice == expected_invoice


def test_journal_entries(odoo_consumer: Consumer):
    consumer = odoo_consumer

    entries = consumer.accounting.JournalEntry.all(
        {
            "unposted_allowed": "false",
            "date_from": "2023-03-01",
            "date_to": "2023-06-01",
            "journal_id": "7",
        },
        limit=2,
    )

    assert entries
