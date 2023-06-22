from typing import ClassVar

from chift.api.mixins import CreateMixin, ListMixin, ReadMixin
from chift.openapi.models import WebhookInstance as WebhookInstanceModel
from chift.openapi.models import WebhookType as WebhookTypeModel


class Webhook(ReadMixin, ListMixin, CreateMixin):
    chift_vertical: ClassVar = "webhooks"
    model = WebhookInstanceModel
    chift_model = None
    extra_path = None
    consumer_id = None
    connection_id = None

    @classmethod
    def get(self, chift_id, client=None):
        return super().get(Webhook, chift_id, client=client)

    @classmethod
    def all(self, client=None):
        return super().all(Webhook, client=client)


class WebhookType(ListMixin):
    chift_vertical: ClassVar = "webhooks"
    chift_model: ClassVar = "list"
    model = WebhookTypeModel
    extra_path = None
    consumer_id = None
    connection_id = None

    @classmethod
    def all(self, client=None):
        return super().all(WebhookType, client=client)
