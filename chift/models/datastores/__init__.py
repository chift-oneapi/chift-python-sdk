from typing import ClassVar

from chift.api.mixins import ListMixin
from chift.openapi.models import Datastore as DatastoreModel


class Datastore(ListMixin):
    chift_vertical: ClassVar = "datastores"
    model = DatastoreModel
    chift_model = None
    extra_path = None
    consumer_id = None
    connection_id = None

    @classmethod
    def all(cls, client=None):
        return super().all(Datastore, client=client)
