from typing import ClassVar

from chift.api.mixins import ReadMixin, UpdateMixin
from chift.openapi.models import SyncConsumer as SyncConsumerModel


class Sync(ReadMixin[SyncConsumerModel], UpdateMixin[SyncConsumerModel]):
    chift_vertical: ClassVar = "syncs"
    chift_model: ClassVar = ""
    model = SyncConsumerModel
