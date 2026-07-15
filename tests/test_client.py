import http.client as httplib

import pytest

from chift.api.client import ChiftClient
from chift.openapi.models import Consumer
from tests.fixtures import client


class _FakeResponse:
    status_code = httplib.OK

    def json(self):
        return {"ok": True}


def _capture_headers(monkeypatch):
    """Patch process_request to capture the headers of the next request."""
    captured = {}

    def fake_process_request(self, request_type, url_path, headers=None, **kw):
        captured.update(headers or {})
        return _FakeResponse()

    monkeypatch.setattr(ChiftClient, "process_request", fake_process_request)
    return captured


def _build_client(chift):
    return ChiftClient(
        client_id=chift.client_id,
        client_secret=chift.client_secret,
        account_id=chift.account_id,
        url_base=chift.url_base,
    )


def test_datalayer_header_sent(chift, monkeypatch):
    captured = _capture_headers(monkeypatch)
    chift_client = _build_client(chift)
    chift_client.datalayer = True

    chift_client.get("/some/path")

    assert captured.get("x-chift-datalayer") == "true"


def test_datalayer_header_if_available(chift, monkeypatch):
    captured = _capture_headers(monkeypatch)
    chift_client = _build_client(chift)
    chift_client.datalayer = "if_available"

    chift_client.get("/some/path")

    assert captured.get("x-chift-datalayer") == "if_available"


def test_datalayer_header_absent_by_default(chift, monkeypatch):
    captured = _capture_headers(monkeypatch)
    chift_client = _build_client(chift)

    chift_client.get("/some/path")

    assert "x-chift-datalayer" not in captured


@pytest.mark.mock_chift_response(client.CONSUMER_ALL, client.CONSUMER_ALL[0])
def test_client_consumer_id(chift):
    chift_client = ChiftClient(
        client_id=chift.client_id,
        client_secret=chift.client_secret,
        account_id=chift.account_id,
        url_base=chift.url_base,
    )

    consumers = chift.Consumer.all(client=chift_client)

    assert consumers

    consumer: Consumer = chift.Consumer.get(
        consumers[0].consumerid, client=chift_client
    )

    assert consumer

    assert consumer.invoicing.Invoice.consumer_id == consumer.consumerid
