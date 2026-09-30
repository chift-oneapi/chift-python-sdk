from typing import ClassVar

from chift.api.mixins import CreateMixin, DeleteMixin, ListMixin, ReadMixin
from chift.openapi.models import Connection as ConnectionModel
from chift.openapi.models import ConnectionLink as ConnectionLinkModel
from chift.openapi.models import DatalayerRefresh as DatalayerRefreshModel


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

    def enable_datalayer(self, connection_id, data=None, client=None) -> dict:
        return super().create(
            data,
            client=client,
            map_model=False,
            extra_path=f"{connection_id}/enable_datalayer",
        )

    def refresh_datalayer(
        self, connection_id, data=None, client=None
    ) -> DatalayerRefreshModel:
        json_data = super().create(
            data,
            client=client,
            map_model=False,
            extra_path=f"{connection_id}/refresh_datalayer",
        )
        return DatalayerRefreshModel(**json_data)

    def disable_datalayer(self, connection_id, client=None) -> None:
        super().create(
            None,
            client=client,
            map_model=False,
            extra_path=f"{connection_id}/disable_datalayer",
        )
