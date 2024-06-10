from typing import ClassVar

from chift.api.mixins import CreateMixin, DeleteMixin, ListMixin, ReadMixin
from chift.openapi.models import Connection as ConnectionModel
from chift.openapi.models import ConnectionLink as ConnectionLinkModel


class Connection(
    ReadMixin[ConnectionModel],
    ListMixin[ConnectionModel],
    CreateMixin[ConnectionLinkModel],
    DeleteMixin,
):
    chift_vertical: ClassVar = "connections"
    chift_model: ClassVar = ""
    model = ConnectionModel

    def create(self, data, client=None, params=None) -> ConnectionLinkModel:
        self.model = ConnectionLinkModel
        return super().create(data, map_model=True, client=client, params=params)
