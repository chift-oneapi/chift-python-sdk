from typing import ClassVar

from chift.api.mixins import CreateMixin, DeleteMixin, ListMixin, ReadMixin
from chift.openapi.models import Flow as FlowModel
from chift.openapi.models import Sync as SyncModel


class Sync(ReadMixin, ListMixin, CreateMixin):
    chift_vertical: ClassVar = "syncs"
    model = SyncModel
    chift_model = None
    extra_path = None
    consumer_id = None
    connection_id = None

    @classmethod
    def get(cls, chift_id, client=None):
        return super().get(Sync, chift_id, client=client)

    @classmethod
    def all(cls, client=None):
        return super().all(Sync, client=client)


class Flow(
    ListMixin[FlowModel], CreateMixin[FlowModel], DeleteMixin, ReadMixin[FlowModel]
):
    chift_vertical: ClassVar = "syncs"
    model = FlowModel
    chift_model = None
    extra_path = None
    consumer_id = None
    connection_id = None

    @classmethod
    def create(self, sync_id, data, client=None):
        self.extra_path = f"{sync_id}/flows"
        return super().create(Flow, data, client=client)

    @classmethod
    def delete(self, sync_id, flow_id, client=None):
        self.extra_path = f"{sync_id}/flows/{flow_id}"
        return super().delete(Flow, chift_id=None, client=client)

    @classmethod
    def trigger(self, sync_id, flow_id, data, client=None):
        self.extra_path = f"{sync_id}/flows/{flow_id}/event"
        return super().create(Flow, data, client=client, map_model=False)

    @classmethod
    def chainexecution(self, sync_id, flow_id, chainexecution_id, client=None):
        self.extra_path = f"/flows/{flow_id}/executions/{chainexecution_id}"
        return super().get(Flow, sync_id, client=client, map_model=False)
