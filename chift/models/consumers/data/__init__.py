from typing import ClassVar

from chift.api.mixins import CreateMixin, ListMixin, UpdateMixin
from chift.openapi.models import Data as DataModel


class Data(
    ListMixin[DataModel],
    CreateMixin[DataModel],
    UpdateMixin[DataModel],
):
    chift_vertical: ClassVar = "datastore"
    chift_model: ClassVar = ""
    model = DataModel

    def get(self, datastore_id, params=None, client=None) -> DataModel:
        self.extra_path = f"{datastore_id}/data"
        return super().all(params=params, client=client)

    def create(self, datastore_id, data, client=None) -> list[DataModel]:
        self.extra_path = f"{datastore_id}/data"
        return [
            DataModel(**item)
            for item in super().create(data, map_model=False, client=client)
        ]

    def update(self, datastore_id, datastoredata_id, data, client=None) -> DataModel:
        self.extra_path = f"{datastore_id}/data/{datastoredata_id}"
        return super().update(None, data, client=client)
