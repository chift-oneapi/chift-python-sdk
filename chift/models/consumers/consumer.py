from __future__ import annotations

from chift.api.mixins import ListMixin, ReadMixin
from chift.openapi.models import Consumer as ConsumerModel


class Consumer(ReadMixin[ConsumerModel], ListMixin[ConsumerModel]):
    chift_vertical = "consumers"
    model = ConsumerModel
    chift_model = None
    extra_path = None
    consumer_id = None
    connection_id = None

    @classmethod
    def get(cls, chift_id, client=None) -> ConsumerModel:
        return super().get(cls, chift_id, client=client)

    @classmethod
    def all(cls, client=None) -> list[ConsumerModel]:
        return super().all(cls, client=client)
