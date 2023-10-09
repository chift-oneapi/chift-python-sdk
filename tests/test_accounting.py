import uuid

import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


def test_analytic_plan(accounting_consumer: Consumer):
    consumer = accounting_consumer

    plans = consumer.accounting.AnalyticPlan.all(limit=2)

    assert plans

    for plan in plans:
        assert plan.id


def test_tax(accounting_consumer: Consumer):
    consumer = accounting_consumer

    taxes = consumer.accounting.Tax.all(limit=2)

    assert taxes

    for tax in taxes:
        assert tax.id


def test_account(accounting_consumer: Consumer):
    consumer = accounting_consumer

    accounts = consumer.accounting.Account.all(limit=2)

    assert accounts

    for account in accounts:
        assert account.number


def test_operation(accounting_consumer: Consumer):
    consumer = accounting_consumer

    operations = consumer.accounting.MiscellaneousOperation.all(limit=2)

    assert operations

    for operation in operations:
        expected_operation = consumer.accounting.MiscellaneousOperation.get(
            operation.id
        )

        assert operation == expected_operation


def test_client(accounting_consumer: Consumer):
    consumer = accounting_consumer

    clients = consumer.accounting.Client.all(limit=2)

    assert clients

    for client in clients:
        expected_client = consumer.accounting.Client.get(client.id)

        assert client == expected_client


def test_update_client(accounting_consumer: Consumer):
    consumer = accounting_consumer

    clients = consumer.accounting.Client.all(limit=2)

    assert clients

    for client in clients:
        current_website = client.website

        updated_client = consumer.accounting.Client.update(
            client.id, {"website": "https://test.com"}
        )
        assert updated_client.website == "https://test.com"

        consumer.accounting.Client.update(
            client.id, {"website": current_website}
        )  # revert
        break  # one is enough


def test_supplier(accounting_consumer: Consumer):
    consumer = accounting_consumer

    suppliers = consumer.accounting.Supplier.all(limit=2)

    assert suppliers

    for supplier in suppliers:
        expected_supplier = consumer.accounting.Supplier.get(supplier.id)

        assert supplier == expected_supplier


def test_invoice(accounting_consumer: Consumer):
    consumer = accounting_consumer

    invoices = consumer.accounting.Invoice.all("customer_invoice", limit=2)

    assert invoices

    for invoice in invoices:
        expected_invoice = consumer.accounting.Invoice.get(invoice.id)

        assert invoice == expected_invoice


def test_journal_entries(pennylane_consumer: Consumer):
    consumer = pennylane_consumer

    journals = consumer.accounting.Journal.all()
    accounts = consumer.accounting.Account.all()

    entry = consumer.accounting.Entry.create(
        {
            "date": "2023-08-01",
            "number": str(uuid.uuid4()),
            "journal_id": journals[0].id,
            "currency": "EUR",
            "items": [
                {
                    "account": accounts[0].number,
                    "account_type": "general_account",
                    "description": "test debit",
                    "debit": 1,
                    "credit": 0,
                },
                {
                    "account": accounts[0].number,
                    "account_type": "general_account",
                    "description": "test credit",
                    "debit": 0,
                    "credit": 1,
                },
            ],
        },
    )

    assert entry

    entries = consumer.accounting.JournalEntry.all(
        {
            "unposted_allowed": "true",
            "date_from": "2023-08-01",
            "date_to": "2023-08-31",
            "journal_id": journals[0].id,
        },
        limit=2,
    )

    assert entries

    # assert entry.id in [entry.id for entry in entries] NOK with caching


def test_journals(accounting_consumer: Consumer):
    consumer = accounting_consumer

    journals = consumer.accounting.Journal.all(
        limit=2,
    )

    for journal in journals:
        assert journal.id


def test_financial_entries(accounting_consumer: Consumer):
    consumer = accounting_consumer

    journals = consumer.accounting.Journal.all()
    accounts = consumer.accounting.Account.all()

    for account in accounts:
        if account.type.value == "other_financial":
            account = account
            break

    for journal in journals:
        if journal.journal_type.value == "financial_operation":
            financial_entry = consumer.accounting.FinancialEntry.create(
                {
                    "date": "2023-08-01",
                    "journal_id": journal.id,
                    "currency": "EUR",
                    "items": [
                        {
                            "type": "general_account",
                            "account_number": account.number,
                            "amount": 1,
                        }
                    ],
                },
            )
            break

    assert financial_entry


def test_outstandings(accounting_consumer: Consumer):
    consumer = accounting_consumer

    with pytest.raises(ChiftException) as e:
        consumer.accounting.Outstanding.all(
            params={"type": "client", "unposted_allowed": "false"},
            limit=2,
        )
    assert e.value.message == "API Resource does not exist"
