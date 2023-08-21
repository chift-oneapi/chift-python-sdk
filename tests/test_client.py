from chift.api.client import ChiftClient
from chift.openapi.models import Consumer


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
