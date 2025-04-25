import pytest

from tests.fixtures import webhook


@pytest.mark.mock_chift_response(
    webhook.WEBHOOK_ALL,
    webhook.WEBHOOK_ALL[0],
)
def test_webhook_instance(chift):
    webhooks = chift.Webhook.all()

    expected_webhook = webhooks[0]

    actual_webhook = chift.Webhook.get(expected_webhook.webhookid)

    assert expected_webhook == actual_webhook


@pytest.mark.mock_chift_response(
    webhook.WEBHOOK_TYPES_ALL,
)
@pytest.mark.skip(reason="possible bug")
def test_webhook_type(chift):
    webhook_type = chift.WebhookType.all()

    assert webhook_type[0].event
