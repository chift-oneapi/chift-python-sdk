import datetime
import uuid

import pytest

from chift.api.client import ChiftClient
from chift.api.exceptions import ChiftException
from chift.api.headers import CombinedDatalayerHeaders, DatalayerHeaders
from chift.openapi.models import Consumer


class _Response:
    def __init__(self, body, headers=None, status_code=200):
        self._body = body
        self.headers = headers or {}
        self.status_code = status_code
        self.text = str(body)

    def json(self):
        return self._body


@pytest.fixture
def serve(monkeypatch):
    """Queue responses for the next requests, served through the real make_request."""
    queue = []

    def fake_process_request(self, request_type, url_path, **kwargs):
        return queue.pop(0)

    monkeypatch.setattr(ChiftClient, "process_request", fake_process_request)
    return queue


@pytest.fixture
def consumer(chift):
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


def _page(items, total, source, synced_at=None, covered_from=None):
    headers = {"X-Chift-Datalayer-Source": source}
    if synced_at:
        headers["X-Chift-Datalayer-Synced-At"] = synced_at
    if covered_from:
        headers["X-Chift-Datalayer-Covered-From"] = covered_from
    return _Response({"items": items, "total": total}, headers)


def test_captures_any_header_case_insensitively(chift, consumer, serve):
    serve.append(_Response({"id": "1"}, {"X-Custom": "abc"}))

    with chift.capture_headers() as captured:
        consumer.pos.Order.get("1", map_model=False)

    assert len(captured) == 1
    assert captured.last["x-custom"] == "abc"
    assert captured.last.method == "GET"
    assert captured.last.path.endswith("/pos/orders/1")
    assert captured.last.status_code == 200
    assert captured.last.datalayer is None


def test_datalayer_headers_are_parsed(chift, consumer, serve):
    serve.append(
        _page(
            [],
            0,
            "datalayer",
            synced_at="2026-09-29T10:00:00+00:00",
            covered_from="2025-01-01",
        )
    )

    with chift.capture_headers() as captured:
        consumer.pos.Order.all(map_model=False, datalayer=True)

    assert captured.last.datalayer == DatalayerHeaders(
        source="datalayer",
        synced_at=datetime.datetime(2026, 9, 29, 10, tzinfo=datetime.timezone.utc),
        covered_from=datetime.date(2025, 1, 1),
    )


def test_datalayer_across_pages_takes_the_worst_case(chift, consumer, serve):
    serve.extend(
        [
            _page(
                [{"id": "1"}],
                3,
                "datalayer",
                synced_at="2026-09-29T10:00:00+00:00",
                covered_from="2025-01-01",
            ),
            _page(
                [{"id": "2"}],
                3,
                "datalayer",
                synced_at="2026-09-29T08:00:00+00:00",
                covered_from="2025-03-01",
            ),
            _page([{"id": "3"}], 3, "classic"),
        ]
    )

    with chift.capture_headers() as captured:
        consumer.pos.Order.all(map_model=False, datalayer="if_available")

    assert len(captured) == 3
    assert captured.datalayer == CombinedDatalayerHeaders(
        source="mixed",
        synced_at=datetime.datetime(2026, 9, 29, 8, tzinfo=datetime.timezone.utc),
        covered_from=datetime.date(2025, 3, 1),
    )


def test_error_response_is_captured(chift, consumer, serve):
    serve.append(
        _Response(
            {"status": "error", "message": "Too many requests"},
            {"Retry-After": "30"},
            status_code=429,
        )
    )

    with chift.capture_headers() as captured:
        with pytest.raises(ChiftException):
            consumer.pos.Order.get("1")

    assert captured.last.status_code == 429
    assert captured.last["retry-after"] == "30"


def test_nested_blocks_both_capture(chift, consumer, serve):
    serve.extend([_Response({"id": "1"}), _Response({"id": "2"})])

    with chift.capture_headers() as outer:
        consumer.pos.Order.get("1", map_model=False)
        with chift.capture_headers() as inner:
            consumer.pos.Order.get("2", map_model=False)

    assert len(outer) == 2
    assert len(inner) == 1


def test_nothing_captured_outside_a_block(chift, consumer, serve):
    serve.extend([_Response({"id": "1"}), _Response({"id": "2"})])

    with chift.capture_headers() as captured:
        consumer.pos.Order.get("1", map_model=False)
    consumer.pos.Order.get("2", map_model=False)

    assert len(captured) == 1


def test_unparseable_freshness_value_stays_readable(chift, consumer, serve):
    serve.append(_page([], 0, "datalayer", synced_at="yesterday"))

    with chift.capture_headers() as captured:
        consumer.pos.Order.all(map_model=False, datalayer=True)

    assert captured.last.datalayer.synced_at is None
    assert captured.last["x-chift-datalayer-synced-at"] == "yesterday"
