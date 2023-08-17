from typing import Generic, TypeVar

from chift.api.client import ChiftClient

T = TypeVar("T")


class BaseMixin(object):
    def __init__(self, consumer_id, connection_id):
        self.chift_vertical = (
            hasattr(self, "chift_vertical") and self.chift_vertical or None
        )
        self.chift_model = hasattr(self, "chift_model") and self.chift_model or None
        self.extra_path = hasattr(self, "extra_path") and self.extra_path or None
        self.consumer_id = consumer_id
        self.connection_id = connection_id


class DeleteMixin(BaseMixin, Generic[T]):
    def delete(self, chift_id, client=None) -> T:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id

        return client.delete_one(
            self.chift_vertical,
            self.chift_model,
            chift_id=chift_id,
            extra_path=self.extra_path,
        )


class ReadMixin(BaseMixin, Generic[T]):
    def get(self, chift_id, client=None, params=None, map_model=True) -> T:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id

        json_data = client.get_one(
            self.chift_vertical,
            self.chift_model,
            chift_id=chift_id,
            extra_path=self.extra_path,
            params=params,
        )

        return self.model(**json_data) if map_model else json_data


class CreateMixin(BaseMixin, Generic[T]):
    def create(self, data, client=None, map_model=True) -> T:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id

        json_data = client.post_one(
            self.chift_vertical, self.chift_model, data, extra_path=self.extra_path
        )

        return self.model(**json_data) if map_model else json_data


class UpdateMixin(BaseMixin, Generic[T]):
    def update(self, chift_id, data, client=None, map_model=True) -> T:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id

        json_data = client.update_one(
            self.chift_vertical,
            self.chift_model,
            chift_id,
            data,
            extra_path=self.extra_path,
        )

        return self.model(**json_data) if map_model else json_data


class PaginationMixin(BaseMixin, Generic[T]):
    def all(self, params=None, client=None, map_model=True, limit=None) -> list[T]:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id

        if not params:
            params = {}

        size = limit if limit and limit < 100 else 100

        all_items = []
        page = 1

        while True:
            json_data = client.get_all(
                self.chift_vertical,
                self.chift_model,
                params={"page": page, "size": size} | params,
                extra_path=self.extra_path,
            )
            all_items.extend(
                [
                    self.model(**item) if map_model else item
                    for item in json_data.get("items", [])
                ]
            )
            page += 1

            if limit and len(all_items) >= limit:
                break

            if len(all_items) >= json_data.get("total", 0) or not json_data.get(
                "items"
            ):
                break

        return all_items


class ListMixin(BaseMixin, Generic[T]):
    def all(self, params=None, client=None) -> list[T]:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id

        json_data = client.get_all(
            self.chift_vertical,
            self.chift_model,
            params=params,
            extra_path=self.extra_path,
        )

        return [self.model(**item) for item in json_data]
