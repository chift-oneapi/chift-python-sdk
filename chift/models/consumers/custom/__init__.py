from typing import ClassVar

from chift.api.mixins import (
    CreateMixin,
    DeleteMixin,
    PaginationMixin,
    ReadMixin,
    UpdateMixin,
)


class CustomRouter:
    def __init__(self, consumer_id, connection_id):
        self.Custom = Custom(consumer_id, connection_id)


class Custom(ReadMixin, CreateMixin, UpdateMixin, PaginationMixin, DeleteMixin):
    chift_vertical: ClassVar = "custom"
    chift_model: ClassVar = ""
    model = None

    def get(self, connector, entity, id, params=None, client=None):
        self.extra_path = f"{connector}/{entity}/{id}"
        return super().get(chift_id=None, map_model=False, params=params, client=client)

    def all(self, connector, entity, params=None, client=None, limit=None):
        self.extra_path = f"{connector}/{entity}"
        return super().all(params=params, map_model=False, client=client, limit=limit)

    def create(self, connector, entity, data, client=None, params=None):
        self.extra_path = f"{connector}/{entity}"
        return super().create(data, map_model=False, client=client, params=params)

    def update(self, connector, entity, id, data, client=None, params=None):
        self.extra_path = f"{connector}/{entity}/{id}"
        return super().update(None, data, map_model=False, client=client, params=params)

    def delete(self, connector, entity, id, client=None, params=None):
        self.extra_path = f"{connector}/{entity}/{id}"
        return super().delete(chift_id=None, client=client, params=params)
