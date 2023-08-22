from typing import ClassVar

from chift.api.mixins import CreateMixin, PaginationMixin, ReadMixin, UpdateMixin


class CustomRouter:
    def __init__(self, consumer_id, connection_id):
        self.Custom = Custom(consumer_id, connection_id)


class Custom(ReadMixin, CreateMixin, UpdateMixin, PaginationMixin):
    chift_vertical: ClassVar = "custom"
    chift_model: ClassVar = ""
    model = None

    def get(self, connector, entity, id, client=None):
        self.extra_path = f"{connector}/{entity}/{id}"
        return super().get(map_model=False, client=client)

    def all(self, connector, entity, params=None, client=None, limit=None):
        self.extra_path = f"{connector}/{entity}"
        return super().all(params=params, map_model=False, client=client, limit=limit)

    def create(self, connector, entity, data, client=None):
        self.extra_path = f"{connector}/{entity}"
        return super().create(data, map_model=False, client=client)

    def update(self, connector, entity, id, data, client=None):
        self.extra_path = f"{connector}/{entity}/{id}"
        return super().update(None, data, map_model=False, client=client)
