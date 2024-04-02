from typing import ClassVar

from chift.api.mixins import CreateMixin, ListMixin, ReadMixin
from chift.openapi.models import Connection as ConnectionModel


class Connection(
    ReadMixin[ConnectionModel], ListMixin[ConnectionModel], CreateMixin[ConnectionModel]
):
    chift_vertical: ClassVar = "connections"
    chift_model: ClassVar = ""
    model = ConnectionModel

    @classmethod
    def create(cls, data, client=None) -> dict:
        return super().create(cls, data, client=client)
