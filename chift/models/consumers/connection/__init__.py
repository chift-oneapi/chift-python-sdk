from typing import ClassVar

from chift.api.mixins import ListMixin, ReadMixin
from chift.openapi.models import Connection as ConnectionModel


class Connection(ReadMixin[ConnectionModel], ListMixin[ConnectionModel]):
    chift_vertical: ClassVar = "connections"
    chift_model: ClassVar = ""
    model = ConnectionModel
