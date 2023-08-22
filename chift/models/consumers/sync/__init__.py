from typing import ClassVar

from chift.api.mixins import ReadMixin
from chift.openapi.models import SyncConsumer as SyncConsumerModel


class Sync(ReadMixin[SyncConsumerModel]):
    chift_vertical: ClassVar = "syncs"
    chift_model: ClassVar = ""
    model = SyncConsumerModel
