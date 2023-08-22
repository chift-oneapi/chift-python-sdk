from typing import ClassVar

from chift.api.mixins import CreateMixin, ListMixin
from chift.openapi.models import Log as LogModel


class Log(ListMixin[LogModel], CreateMixin[LogModel]):
    chift_vertical: ClassVar = "logs"
    chift_model: ClassVar = ""
    model = LogModel

    def create(self, data: list, client=None):
        return super().create(data, map_model=False, client=client)
