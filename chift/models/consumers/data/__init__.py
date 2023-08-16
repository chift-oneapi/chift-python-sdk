from typing import ClassVar

from chift.api.mixins import CreateMixin, ListMixin, UpdateMixin
from chift.openapi.models import Data as DataModel


class DataRouter:
    def __init__(self, consumer_id, connection_id):
        self.Data = Data(consumer_id, connection_id)


class Data(
    ListMixin[DataModel],
    CreateMixin[DataModel],
    UpdateMixin[DataModel],
):
    chift_vertical: ClassVar = "datastore"
    chift_model: ClassVar = ""
    model = DataModel

    def get(self, datastore_id, params=None, client=None):
        self.extra_path = f"{datastore_id}/data"
        return super().all(params=params, client=client)

    def create(self, datastore_id, data, client=None):
        self.extra_path = f"{datastore_id}/data"
        return super().create(data, map_model=False, client=client)

    def update(self, datastore_id, data, client=None):
        self.extra_path = f"{datastore_id}/data"
        return super().update(data, map_model=False, client=client)
