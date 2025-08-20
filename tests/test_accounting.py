import uuid

import pytest

from chift.openapi.models import Consumer
from tests.fixtures import accounting


@pytest.mark.mock_chift_response(accounting.ANALYTIC_PLAN_ALL)
def test_analytic_plan(accounting_consumer: Consumer):
    consumer = accounting_consumer

    plans = consumer.accounting.AnalyticPlan.all(limit=2)

    assert plans

    for plan in plans:
        assert plan.id


@pytest.mark.mock_chift_response(accounting.TAX_ALL)
def test_tax(accounting_consumer: Consumer):
    consumer = accounting_consumer

    taxes = consumer.accounting.Tax.all(limit=2)

    assert taxes

    for tax in taxes:
        assert tax.id


@pytest.mark.mock_chift_response(accounting.ACCOUNT_ALL)
def test_account(accounting_consumer: Consumer):
    consumer = accounting_consumer

    accounts = consumer.accounting.Account.all(limit=2)

    assert accounts

    for account in accounts:
        assert account.number


@pytest.mark.mock_chift_response(
    accounting.MISCELLANEOUS_OPERATION_ALL,
    accounting.MISCELLANEOUS_OPERATION_ALL["items"][0],
    accounting.MISCELLANEOUS_OPERATION_ALL["items"][1],
)
def test_operation(accounting_consumer: Consumer):
    consumer = accounting_consumer

    operations = consumer.accounting.MiscellaneousOperation.all(limit=2)

    assert operations

    for operation in operations:
        expected_operation = consumer.accounting.MiscellaneousOperation.get(
            operation.id
        )

        assert operation == expected_operation


@pytest.mark.mock_chift_response(
    accounting.CLIENT_ALL,
    accounting.CLIENT_ALL["items"][0],
    accounting.CLIENT_ALL["items"][1],
)
def test_client(accounting_consumer: Consumer):
    consumer = accounting_consumer

    clients = consumer.accounting.Client.all(limit=2)

    assert clients

    for client in clients:
        expected_client = consumer.accounting.Client.get(client.id)

        assert client == expected_client


@pytest.mark.mock_chift_response(accounting.CLIENT_ALL, accounting.CLIENT_UPDATE)
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


@pytest.mark.mock_chift_response(
    accounting.SUPPLIER_ALL,
    accounting.SUPPLIER_ALL["items"][0],
    accounting.SUPPLIER_ALL["items"][1],
)
def test_supplier(accounting_consumer: Consumer):
    consumer = accounting_consumer

    suppliers = consumer.accounting.Supplier.all(limit=2)

    assert suppliers

    for supplier in suppliers:
        expected_supplier = consumer.accounting.Supplier.get(supplier.id)

        assert supplier == expected_supplier


@pytest.mark.mock_chift_response(
    accounting.INVOICE_ALL,
    accounting.INVOICE_ALL["items"][0],
    accounting.INVOICE_ALL["items"][1],
)
def test_invoice(accounting_consumer: Consumer):
    consumer = accounting_consumer

    invoices = consumer.accounting.Invoice.all("customer_invoice", limit=2)

    assert invoices

    for invoice in invoices:
        expected_invoice = consumer.accounting.Invoice.get(invoice.id)

        assert invoice == expected_invoice


@pytest.mark.mock_chift_response(
    accounting.JOURNAL_ALL, accounting.ACCOUNT_ALL, accounting.ENTRY_CREATE
)
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
    # TODO: fix this part
    # entries = consumer.accounting.JournalEntry.all(
    #     {
    #         "unposted_allowed": "true",
    #         "date_from": "2023-08-01",
    #         "date_to": "2023-08-31",
    #         "journal_id": journals[0].id,
    #     },
    #     limit=2,
    # )
    #
    # assert entries

    # assert entry.id in [entry.id for entry in entries] NOK with caching


@pytest.mark.mock_chift_response(accounting.JOURNAL_ALL)
def test_journals(accounting_consumer: Consumer):
    consumer = accounting_consumer

    journals = consumer.accounting.Journal.all(
        limit=2,
    )

    for journal in journals:
        assert journal.id


@pytest.mark.mock_chift_response(
    accounting.JOURNAL_ALL, accounting.ACCOUNT_ALL, accounting.FINANCIAL_ENTRY_CREATE
)
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
                            "account_type": "general_account",
                            "account": account.number,
                            "amount": 1,
                        }
                    ],
                },
            )
            break

    assert financial_entry


@pytest.mark.mock_chift_response(accounting.OUTSTANDING_ALL)
def test_outstandings(accounting_consumer: Consumer):
    consumer = accounting_consumer

    outstandings = consumer.accounting.Outstanding.all(
        params={"type": "client", "unposted_allowed": "false"},
        limit=2,
    )

    assert outstandings

    for outstanding in outstandings:
        assert outstanding.id


@pytest.mark.mock_chift_response(accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_ALL)
def test_analytic_account_multi_plan_all(accounting_consumer: Consumer):
    consumer = accounting_consumer

    accounts = consumer.accounting.AnalyticAccountMultiPlan.all(limit=2)

    assert accounts
    assert len(accounts) == 2

    for account in accounts:
        assert account.id
        assert account.name
        assert account.code is None
        assert account.analytic_plan


@pytest.mark.mock_chift_response(
    accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_ALL,
    accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_ALL["items"][0],
    accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_ALL["items"][1],
)
def test_analytic_account_multi_plan_get(accounting_consumer: Consumer):
    consumer = accounting_consumer

    accounts = consumer.accounting.AnalyticAccountMultiPlan.all(limit=2)

    assert accounts

    for account in accounts:
        expected_account = consumer.accounting.AnalyticAccountMultiPlan.get(
            account.id, account.analytic_plan
        )

        assert account == expected_account
        assert expected_account.id == account.id
        assert expected_account.analytic_plan == account.analytic_plan


@pytest.mark.mock_chift_response(accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_CREATE)
def test_analytic_account_multi_plan_create(accounting_consumer: Consumer):
    consumer = accounting_consumer

    new_account_data = {
        "name": "New Project Analysis",
        "code": "NEW-001",
        "active": True,
        "currency": "EUR",
    }

    created_account = consumer.accounting.AnalyticAccountMultiPlan.create(
        new_account_data, "plan-001"
    )

    assert created_account
    assert created_account.id == accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_CREATE["id"]
    assert created_account.name == accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_CREATE["name"]
    assert created_account.code == accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_CREATE["code"]
    assert (
        created_account.analytic_plan
        == accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_CREATE["analytic_plan"]
    )
    assert created_account.active is True


@pytest.mark.mock_chift_response(
    accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_ALL,
    accounting.ANALYTIC_ACCOUNT_MULTI_PLAN_UPDATE,
)
def test_analytic_account_multi_plan_update(accounting_consumer: Consumer):
    consumer = accounting_consumer

    accounts = consumer.accounting.AnalyticAccountMultiPlan.all(limit=1)

    assert accounts

    account = accounts[0]
    original_name = account.name

    updated_account = consumer.accounting.AnalyticAccountMultiPlan.update(
        account.id, account.analytic_plan, {"name": "Updated Marketing Campaign"}
    )

    assert updated_account
    assert updated_account.id == account.id
    assert updated_account.name == "Updated Marketing Campaign"
    assert updated_account.analytic_plan == account.analytic_plan
    assert updated_account.name != original_name
