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
        return super().all(
            params=params, client=client, extra_path=f"{datastore_id}/data"
        )

    def create(self, datastore_id, data, client=None, params=None) -> list[DataModel]:
        return [
            DataModel(**item)
            for item in super().create(
                data,
                map_model=False,
                client=client,
                params=params,
                extra_path=f"{datastore_id}/data",
            )
        ]

    def update(
        self, datastore_id, datastoredata_id, data, client=None, params=None
    ) -> DataModel:
        return super().update(
            None,
            data,
            client=client,
            params=params,
            extra_path=f"{datastore_id}/data/{datastoredata_id}",
        )

    def delete(self, datastore_id, datastoredata_id, client=None, params=None):
        return super().delete(
            None,
            client=client,
            params=params,
            extra_path=f"{datastore_id}/data/{datastoredata_id}",
        )
