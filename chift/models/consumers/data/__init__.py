from typing import ClassVar

from chift.api.mixins import CreateMixin, DeleteMixin, ListMixin, UpdateMixin
from chift.openapi.models import Data as DataModel


class Data(
    ListMixin[DataModel],
    CreateMixin[DataModel],
    UpdateMixin[DataModel],
    DeleteMixin,
):
    chift_vertical: ClassVar = "datastore"
    chift_model: ClassVar = ""
    model = DataModel

    def get(self, datastore_id, params=None, client=None) -> list[DataModel]:
        self.extra_path = f"{datastore_id}/data"
        return super().all(params=params, client=client)

    def create(self, datastore_id, data, client=None, params=None) -> list[DataModel]:
        self.extra_path = f"{datastore_id}/data"
        return [
            DataModel(**item)
            for item in super().create(
                data, map_model=False, client=client, params=params
            )
        ]

    def update(
        self, datastore_id, datastoredata_id, data, client=None, params=None
    ) -> DataModel:
        self.extra_path = f"{datastore_id}/data/{datastoredata_id}"
        return super().update(None, data, client=client, params=params)

    def delete(self, datastore_id, datastoredata_id, client=None, params=None):
        self.extra_path = f"{datastore_id}/data/{datastoredata_id}"
        return super().delete(None, client=client, params=params)
