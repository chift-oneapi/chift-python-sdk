"""Regression tests for request-shaping state leaking between calls.

Model classes are instantiated once per vertical router, and callers keep that router for a
whole run (e.g. a sync flow storing ``consumer.accounting``), so anything an override sets on
the instance must not survive the call. Invoice.all() leaving ``extra_path="type/..."`` behind
sent the next create() to accounting/invoices/type/{invoice_type} - a GET-only route whose bare
404 looks like a missing invoice.
"""

import uuid

import pytest

from chift.api.client import ChiftClient
from chift.openapi.models import Consumer
from tests.fixtures import accounting


@pytest.fixture
def recorder(chift, monkeypatch):
    """Record every (method, path) and serve the queued responses."""
    calls = []
    responses = []

    def fake_make_request(self, method, path, **kwargs):
        calls.append((method, path))
        return responses[len(calls) - 1] if len(calls) <= len(responses) else {}

    monkeypatch.setattr(ChiftClient, "make_request", fake_make_request)
    return calls, responses


@pytest.fixture
def accounting_api(chift):
    # a router held for the whole run, like the sync flows do
    return Consumer(consumerid=uuid.uuid4(), name="Consumer").accounting


def paths(calls, method):
    return [path for call_method, path in calls if call_method == method]


def test_invoice_all_does_not_leak_into_create(recorder, accounting_api):
    calls, responses = recorder
    responses.append({"items": [], "total": 0})

    accounting_api.Invoice.all("customer_invoice")
    accounting_api.Invoice.create({"invoice_number": "INV-1"}, map_model=False)

    assert paths(calls, "GET")[0].endswith("/accounting/invoices/type/customer_invoice")
    assert paths(calls, "POST") == [paths(calls, "GET")[0].split("/type/")[0]]


def test_invoice_all_does_not_leak_into_get(recorder, accounting_api):
    calls, responses = recorder
    responses.append({"items": [], "total": 0})

    accounting_api.Invoice.all("customer_invoice")
    accounting_api.Invoice.get("invoice-001", map_model=False)

    assert paths(calls, "GET")[1].endswith("/accounting/invoices/invoice-001")


def test_invoice_multi_plan_all_does_not_leak_into_create(recorder, accounting_api):
    """The analytic variant of the same route pair: POST-only vs GET-only."""
    calls, responses = recorder
    responses.append({"items": [], "total": 0})

    accounting_api.InvoiceMultiPlan.all("customer_invoice")
    accounting_api.InvoiceMultiPlan.create({"invoice_number": "INV-1"}, map_model=False)

    assert paths(calls, "GET")[0].endswith(
        "/accounting/invoices/multi-analytic-plans/type/customer_invoice"
    )
    assert paths(calls, "POST")[0].endswith("/accounting/invoices/multi-analytic-plans")


def test_iter_all_keeps_extra_path_across_pages(recorder, accounting_api):
    calls, responses = recorder
    first, second = accounting.INVOICE_ALL["items"][:2]
    responses.extend([{"items": [first], "total": 2}, {"items": [second], "total": 2}])

    invoices = list(accounting_api.Invoice.iter_all("customer_invoice"))

    assert len(invoices) == 2
    assert len(paths(calls, "GET")) == 2
    assert all(
        path.endswith("/accounting/invoices/type/customer_invoice")
        for path in paths(calls, "GET")
    )


def test_create_while_iterating_keeps_pagination_scope(recorder, accounting_api):
    """A create() made from inside an iter_all() loop must not retarget the next page."""
    calls, responses = recorder
    first, second = accounting.INVOICE_ALL["items"][:2]
    responses.extend(
        [
            {"items": [first], "total": 2},
            {"items": [], "total": 0},  # the create
            {"items": [second], "total": 2},
        ]
    )

    invoice = accounting_api.Invoice
    for _ in invoice.iter_all("customer_invoice"):
        invoice.create({"invoice_number": "INV-1"}, map_model=False)

    assert paths(calls, "POST") == [
        paths(calls, "GET")[0].split("/type/")[0],
        paths(calls, "GET")[0].split("/type/")[0],
    ]
    assert paths(calls, "GET")[1].endswith("/accounting/invoices/type/customer_invoice")


def test_entry_all_does_not_leak_into_create(recorder, accounting_api):
    """Entry.all() reads journal/entries/multi-analytic-plans, which is GET-only."""
    calls, responses = recorder
    responses.append({"items": [], "total": 0})

    accounting_api.Entry.all()
    accounting_api.Entry.create({"journal_id": "1"}, map_model=False)

    assert paths(calls, "GET")[0].endswith(
        "/accounting/journal/entries/multi-analytic-plans"
    )
    assert paths(calls, "POST")[0].endswith("/accounting/journal-entries")


def test_attachment_create_does_not_leak_into_the_next_call(recorder, accounting_api):
    calls, _ = recorder

    accounting_api.Attachment.create("invoice-001", {"base64_string": "x"})
    accounting_api.Attachment.all()
    accounting_api.Attachment.upload({"base64_string": "x"})

    # accounting_add_attachment lives on invoices/pdf/{invoice_id}; attachments is the GET list
    assert paths(calls, "POST")[0].endswith("/accounting/invoices/pdf/invoice-001")
    assert paths(calls, "GET")[0].endswith("/accounting/attachments")
    assert paths(calls, "POST")[1].endswith("/accounting/attachments")


def test_flow_trigger_does_not_leak_on_the_class(recorder, chift):
    """Flow's managers are classmethods, so a leak there outlived the whole process."""
    calls, responses = recorder
    responses.extend([{}, {"id": "flow-1", "name": "flow"}])

    chift.Flow.trigger("sync-1", "flow-1", {"data": 1})
    chift.Flow.create("sync-1", {"name": "flow"})

    assert paths(calls, "POST") == [
        "/syncs/sync-1/flows/flow-1/event",
        "/syncs/sync-1/flows",
    ]
