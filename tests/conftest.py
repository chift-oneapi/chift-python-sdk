import os
import uuid

import pytest

import chift as package
from chift.api.client import ChiftClient
from chift.openapi.models import Consumer


@pytest.fixture
def chift():
    package.client_secret = os.environ.get("CHIFT_TESTING_CLIENTSECRET", "unit")
    package.client_id = os.environ.get("CHIFT_TESTING_CLIENTID", "unit")
    package.account_id = os.environ.get("CHIFT_TESTING_ACCOUNTID", "unit")
    package.url_base = os.environ.get("CHIFT_BACKBONE_API", "unit")
    return package


@pytest.fixture
def evoliz_consumer(chift):
    # get evoliz connection
    # return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def pennylane_consumer(chift):
    # get pennylane v2 connection
    # return chift.Consumer.get("e7a0051b-b314-4961-861d-3b65749fd33b")
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def accounting_consumer(chift):
    # return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def pos_consumer(chift):
    # return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def ecommerce_consumer(chift):
    # return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def payment_consumer(chift):
    # return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def custom_regate_consumer(chift):
    # return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def two_connections_consumer(chift):
    # get consumer wth 2 connections for one vertical
    # return chift.Consumer.get("46ec75e8-4d79-4d63-8e96-99d2c924d89a")
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def invoicing_consumer(chift):
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture
def test_consumer(chift):
    return Consumer(consumerid=uuid.uuid4(), name="Consumer")


@pytest.fixture(autouse=True)
def _patch_chift_client(monkeypatch, request):
    marker = request.node.get_closest_marker("mock_chift_response")
    if not marker:
        return
    raw = marker.args
    if len(raw) == 1 and isinstance(raw[0], (list, tuple)):
        responses = list(raw[0])
    else:
        responses = list(raw)
    iterator = iter(responses)

    def fake_make_request(self, method, path, **kw):
        try:
            resp = next(iterator)
        except StopIteration:
            resp = responses[-1]
        if isinstance(resp, Exception):
            raise resp
        return resp

    monkeypatch.setattr(ChiftClient, "make_request", fake_make_request)
