from typing import ClassVar

from chift.api.mixins import ListMixin, ReadMixin
from chift.openapi.models import Connection as ConnectionModel


class ConnectionRouter:
    def __init__(self, consumer_id, connection_id):
        self.Connection = Connection(consumer_id, connection_id)


class Connection(ReadMixin[ConnectionModel], ListMixin[ConnectionModel]):
    chift_vertical: ClassVar = "connections"
    chift_model: ClassVar = ""
    model = ConnectionModel
