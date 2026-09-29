import http.client as httplib
import uuid
from datetime import timedelta

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


def _capture_params(monkeypatch):
    """Patch process_request to capture the params of the next request."""
    captured = {}

    def fake_process_request(self, request_type, url_path, params=None, **kw):
        captured.update(params or {})
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


def test_datalayer_max_staleness_header_sent(chift, monkeypatch):
    captured = _capture_headers(monkeypatch)
    chift_client = _build_client(chift)
    chift_client.datalayer = True
    chift_client.datalayer_max_staleness = "PT15M"

    chift_client.get("/some/path")

    assert captured.get("x-chift-datalayer-max-staleness") == "PT15M"


def test_datalayer_max_staleness_timedelta_as_iso_duration(chift, monkeypatch):
    captured = _capture_headers(monkeypatch)
    chift_client = _build_client(chift)
    chift_client.datalayer = True
    chift_client.datalayer_max_staleness = timedelta(hours=1, minutes=30)

    chift_client.get("/some/path")

    assert captured.get("x-chift-datalayer-max-staleness") == "PT5400S"


def test_datalayer_max_staleness_reset_after_request(chift, monkeypatch):
    captured = _capture_headers(monkeypatch)
    chift_client = _build_client(chift)
    chift_client.datalayer = True
    chift_client.datalayer_max_staleness = "PT15M"
    chift_client.get("/some/path")
    captured.clear()

    chift_client.get("/some/path")

    assert "x-chift-datalayer-max-staleness" not in captured


def test_accounting_invoice_all_forwards_datalayer_options(chift, monkeypatch):
    captured = {}

    class _PageResponse(_FakeResponse):
        def json(self):
            return {"items": [], "total": 0}

    def fake_process_request(self, request_type, url_path, headers=None, **kw):
        captured.update(headers or {})
        return _PageResponse()

    monkeypatch.setattr(ChiftClient, "process_request", fake_process_request)
    consumer = Consumer(consumerid=uuid.uuid4(), name="Consumer")

    consumer.accounting.Invoice.all(
        "customer_invoice",
        client=_build_client(chift),
        datalayer="if_available",
        max_staleness="PT1H",
    )

    assert captured.get("x-chift-datalayer") == "if_available"
    assert captured.get("x-chift-datalayer-max-staleness") == "PT1H"


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


def test_bool_query_params_normalized_to_lowercase(chift, monkeypatch):
    # Regression: requests.Session stringifies bool params as "True"/"False", while httpx
    # (the test_client engine) lowercases them. The API only accepts lowercase, so make_request
    # must normalize bools itself rather than relying on whichever engine handles the request.
    captured = _capture_params(monkeypatch)
    chift_client = _build_client(chift)

    chift_client.get(
        "/some/path", params={"unposted_allowed": False, "other": True, "kept": "x"}
    )

    assert captured == {"unposted_allowed": "false", "other": "true", "kept": "x"}


def test_consumer_create_classmethod_resolves_create_path(chift, monkeypatch):
    # Regression: Consumer.create() is a classmethod, so CreateMixin.create must resolve the
    # create path without relying on BaseMixin.__init__ having set chift_model_create.
    captured = {}

    def fake_post_one(self, vertical, model, data, extra_path=None, params=None):
        captured["vertical"] = vertical
        captured["model"] = model
        return {"consumerid": "00000000-0000-0000-0000-000000000001", **data}

    monkeypatch.setattr(ChiftClient, "post_one", fake_post_one)
    chift_client = _build_client(chift)

    consumer = chift.Consumer.create({"name": "Acme"}, client=chift_client)

    assert captured["vertical"] == "consumers"
    assert captured["model"] is None
    assert consumer.name == "Acme"
