import os

import pytest

import chift as package


@pytest.fixture
def chift():
    package.client_secret = os.environ["CHIFT_TESTING_CLIENTSECRET"]
    package.client_id = os.environ["CHIFT_TESTING_CLIENTID"]
    package.account_id = os.environ["CHIFT_TESTING_ACCOUNTID"]
    package.url_base = os.environ["CHIFT_BACKBONE_API"]
    return package


@pytest.fixture
def evoliz_consumer(chift):
    # get evoliz connection
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def pennylane_consumer(chift):
    # get pennylane v2 connection
    return chift.Consumer.get("e7a0051b-b314-4961-861d-3b65749fd33b")


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
def payment_consumer(chift):
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def custom_regate_consumer(chift):
    return chift.Consumer.get("0740d8ad-1920-48c6-8909-c0ea8f8be19e")


@pytest.fixture
def two_connections_consumer(chift):
    # get consumer wth 2 connections for one vertical
    return chift.Consumer.get("46ec75e8-4d79-4d63-8e96-99d2c924d89a")
