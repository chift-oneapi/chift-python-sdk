from typing import ClassVar

from chift.api.mixins import ListMixin
from chift.openapi.models import Integration as IntegrationModel


class Integration(ListMixin):
    chift_vertical: ClassVar = "integrations"
    model = IntegrationModel
    chift_model = None
    extra_path = None
    consumer_id = None
    connection_id = None

    @classmethod
    def all(self, client=None):
        return super().all(Integration, client=client)
