import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


def test_find_one_evoliz_connection(chift):
    consumers = chift.Consumer.all()

    for consumer in consumers:
        connections = consumer.Connection.all()

        for connection in connections:
            if connection.integration == "Evoliz":
                return

    raise Exception("No connection found for Evoliz.")


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
