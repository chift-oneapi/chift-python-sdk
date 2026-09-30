import uuid

import pytest

from chift.api.client import ChiftClient
from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer, DatalayerRefresh


@pytest.mark.skip(reason="no evoliz connection in test environment")
def test_find_one_evoliz_connection(chift):
    consumers = chift.Consumer.all()

    for consumer in consumers:
        connections = consumer.Connection.all()

        for connection in connections:
            if connection.integration == "Evoliz":
                return

    raise Exception("No connection found for Evoliz.")


@pytest.mark.skip(reason="dont make sens in unit testing")
def test_multi_connections(two_connections_consumer: Consumer):
    # a consumer with 2 connections
    consumer = two_connections_consumer

    # will raise if no connectionid is set
    with pytest.raises(ChiftException) as e:
        consumer.invoicing.Invoice.all()

    assert e.value.message == "The connection is not correctly configured"

    connections = consumer.Connection.all()
    active_connection = list(
        filter(lambda conn: conn.status.value == "active", connections)
    )

    # will find invoices if one of the consumers set
    consumer.connectionid = str(active_connection[0].connectionid)
    invoices = consumer.invoicing.Invoice.all()
    invoice = invoices[0]

    # will raise if we try to find the invoice of one connection in the other
    consumer.connectionid = str(active_connection[1].connectionid)
    with pytest.raises(ChiftException) as e:
        consumer.invoicing.Invoice.get(invoice.id)

    assert e.value.message == "The invoice doesn't exist."


@pytest.fixture
def recorded_requests(monkeypatch):
    calls = []
    responses = []

    def fake_make_request(self, method, path, data=None, **kwargs):
        calls.append((method, path, data))
        return responses.pop(0)

    monkeypatch.setattr(ChiftClient, "make_request", fake_make_request)
    return calls, responses


@pytest.fixture
def consumer(chift):
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


def test_enable_datalayer(consumer, recorded_requests):
    calls, responses = recorded_requests
    responses.append({})
    body = {"fiscal_years_back": 1, "entity_filter": {"folder_ids": ["F1"]}}

    consumer.Connection.enable_datalayer("conn-1", body)

    assert calls == [
        (
            "POST",
            f"/consumers/{consumer.consumerid}/connections/conn-1/enable_datalayer",
            body,
        )
    ]


def test_refresh_datalayer(consumer, recorded_requests):
    calls, responses = recorded_requests
    responses.append(
        {
            "status": "success",
            "message": "Flow triggered",
            "data": {"executionid": "e1"},
        }
    )

    result = consumer.Connection.refresh_datalayer(
        "conn-1", {"force_from_date": "2026-01-01"}
    )

    assert calls == [
        (
            "POST",
            f"/consumers/{consumer.consumerid}/connections/conn-1/refresh_datalayer",
            {"force_from_date": "2026-01-01"},
        )
    ]
    assert isinstance(result, DatalayerRefresh)
    assert result.data == {"executionid": "e1"}


def test_disable_datalayer(consumer, recorded_requests):
    calls, responses = recorded_requests
    responses.append(True)  # 204

    assert consumer.Connection.disable_datalayer("conn-1") is None
    assert calls == [
        (
            "POST",
            f"/consumers/{consumer.consumerid}/connections/conn-1/disable_datalayer",
            None,
        )
    ]
