import datetime

import pytest

from chift.api.client import ChiftClient
from chift.openapi.models import Consumer
from tests.fixtures import spend_management as fixtures


@pytest.mark.mock_chift_response([fixtures.LEGAL_ENTITIES_ALL])
def test_legal_entities(test_consumer: Consumer):
    legal_entities = test_consumer.spend_management.LegalEntity.all()

    assert [entity.name for entity in legal_entities] == ["Chift SRL"]


@pytest.mark.mock_chift_response(fixtures.LEDGER_ACCOUNTS_ALL)
def test_ledger_accounts(test_consumer: Consumer):
    accounts = test_consumer.spend_management.LedgerAccount.all()

    assert [account.number for account in accounts] == ["601000", "625100"]


@pytest.mark.mock_chift_response(fixtures.PAYABLES_ALL)
def test_payables(test_consumer: Consumer):
    payables = test_consumer.spend_management.Payable.all(
        params={"payable_type": "supplier_invoice", "export_status": "to_export"}
    )

    payable = payables[0]
    assert (payable.id, payable.payable_date, payable.lines[0].tax_id) == (
        "inv_paper",
        datetime.date(2026, 9, 2),
        "vat_21",
    )


@pytest.mark.mock_chift_response(fixtures.FINANCIAL_MOVEMENTS_ALL)
def test_financial_movements(test_consumer: Consumer):
    movements = test_consumer.spend_management.FinancialMovement.all()

    assert [allocation.payable_id for allocation in movements[0].allocations] == [
        "inv_paper"
    ]


def test_mark_payable_as_exported_patches_its_route(
    test_consumer: Consumer, monkeypatch
):
    requests = []

    def fake_make_request(self, method, path, **kwargs):
        requests.append((method, path))
        return fixtures.PAYABLES_ALL["items"][0] | {"export_status": "exported"}

    monkeypatch.setattr(ChiftClient, "make_request", fake_make_request)

    payable = test_consumer.spend_management.Payable.mark_as_exported("inv_paper")

    assert payable.export_status.value == "exported"
    assert requests == [
        (
            "PATCH",
            f"/consumers/{test_consumer.consumerid}/spend_management/payables/inv_paper/mark-as-exported",
        )
    ]


@pytest.mark.mock_chift_response(fixtures.SUPPLIERS_ALL)
def test_suppliers(test_consumer: Consumer):
    suppliers = test_consumer.spend_management.Supplier.all()

    assert [(supplier.id, supplier.external_reference) for supplier in suppliers] == [
        ("sup_office", "OFFICE01")
    ]
