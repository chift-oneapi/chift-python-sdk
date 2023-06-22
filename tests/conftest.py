import pytest

import chift as package


@pytest.fixture
def chift():
    package.client_secret = "Spht8g8zMYWHTRaT1Qwy"
    package.client_id = "pZMQxOJJ6tl1716"
    package.account_id = "a8bfa890-e7ab-480f-9ae1-4c685f2a2a76"
    package.url_base = "http://localhost:8000"
    return package


@pytest.fixture
def evoliz_consumer(chift):
    # get evoliz connection
    return chift.Consumer.get("0e260397-997e-4791-a674-90ff6dab7caa")


@pytest.fixture
def odoo_consumer(chift):
    # get odoo connection
    return chift.Consumer.get("67e2e902-78e7-4904-bb77-1d25dd57e373")


@pytest.fixture
def zelty_consumer(chift):
    # get zelty connection
    return chift.Consumer.get("595fb2a2-2eee-4f55-bfd1-003a8c4e73b1")


@pytest.fixture
def woocommerce_consumer(chift):
    # get woocommerce connection
    return chift.Consumer.get("b32c1f6d-7277-402c-b5a7-7b510871f14c")


@pytest.fixture
def two_connections_consumer(chift):
    # get consumer wth 2 connections for one vertical
    return chift.Consumer.get("995d0b31-4328-49c6-884d-4b82ea7c60e6")


@pytest.fixture
def sync_consumer(chift):
    # get consumer with a sync
    return chift.Consumer.get("4b7992d3-8b06-4dc7-9c32-3cc008ad4843")


@pytest.fixture
def sync(chift):
    return chift.Sync.get("0c294e89-068a-4629-9d9c-424f2a930f39")
