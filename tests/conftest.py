import pytest

import chift as package


@pytest.fixture
def chift():
    package.client_secret = "FBVxDtiOjb91H9j4XPh4"
    package.client_id = "Iy3H8C34WKSvN2J"
    package.account_id = "187cc583-9bea-4fc7-ba87-a2febe3eae46"
    package.url_base = "https://public-api-test.chift.site"
    return package


@pytest.fixture
def invoicing_consumer(chift):
    # get evoliz connection
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def accounting_consumer(chift):
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def pos_consumer(chift):
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def ecommerce_consumer(chift):
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def custom_regate_consumer(chift):
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def two_connections_consumer(chift):
    # get consumer wth 2 connections for one vertical
    return chift.Consumer.get("bccbe8ed-a2eb-431b-9ba9-7264557fbafd")


@pytest.fixture
def sync_consumer(chift):
    # get consumer with a sync
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def sync(chift):
    return chift.Sync.get("0bf973a7-22e2-4cef-8ae9-c80e4104320a")
