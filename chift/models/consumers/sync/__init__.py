from typing import ClassVar

from chift.api.mixins import ReadMixin
from chift.openapi.models import SyncConsumer as SyncConsumerModel


class SyncRouter:
    def __init__(self, consumer_id, connection_id):
        self.Sync = Sync(consumer_id, connection_id)


class Sync(ReadMixin[SyncConsumerModel]):
    chift_vertical: ClassVar = "syncs"
    chift_model: ClassVar = ""
    model = SyncConsumerModel
