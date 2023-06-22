def test_webhook_instance(chift):
    webhooks = chift.Webhook.all()

    expected_webhook = webhooks[0]

    actual_webhook = chift.Webhook.get(expected_webhook.webhookid)

    assert expected_webhook == actual_webhook


def test_webhook_type(chift):
    webhook_type = chift.WebhookType.all()

    assert webhook_type[0].event
