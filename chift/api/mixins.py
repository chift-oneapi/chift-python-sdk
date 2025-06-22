from typing import Any, Generator, Generic, Literal, TypeVar, overload

from chift.api.client import ChiftClient
from chift.openapi.models import ObjectWithRawData

T = TypeVar("T")


class BaseMixin(object):
    def __init__(self, consumer_id, connection_id):
        self.chift_vertical = (
            hasattr(self, "chift_vertical") and self.chift_vertical or None
        )
        self.chift_model = hasattr(self, "chift_model") and self.chift_model or None
        self.chift_model_create = (
            hasattr(self, "chift_model_create")
            and self.chift_model_create
            or self.chift_model
        )
        self.extra_path = hasattr(self, "extra_path") and self.extra_path or None
        self.consumer_id = consumer_id
        self.connection_id = connection_id


class DeleteMixin(BaseMixin, Generic[T]):
    def delete(self, chift_id, client=None, params=None, client_request_id=None) -> T:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id
        client.raw_data = False
        client.client_request_id = client_request_id

        return client.delete_one(
            self.chift_vertical,
            self.chift_model,
            chift_id=chift_id,
            extra_path=self.extra_path,
            params=params,
        )


class ReadMixin(BaseMixin, Generic[T]):
    @overload
    def get(
        self,
        chift_id,
        client=None,
        params=None,
        map_model: Literal[True] = True,
        raw_data: Literal[False] = False,
    ) -> T: ...

    @overload
    def get(
        self,
        chift_id,
        client=None,
        params=None,
        map_model: Literal[False] = False,
        raw_data: Literal[False] = False,
    ) -> dict: ...

    @overload
    def get(
        self,
        chift_id,
        client=None,
        params=None,
        map_model: Literal[True] = True,
        raw_data: Literal[True] = True,
    ) -> ObjectWithRawData[T]: ...

    @overload
    def get(
        self,
        chift_id,
        client=None,
        params=None,
        map_model: Literal[False] = False,
        raw_data: Literal[True] = True,
    ) -> dict: ...

    def get(
        self, chift_id, client=None, params=None, map_model=True, raw_data=False
    ) -> T | dict | ObjectWithRawData[T]:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id
        client.raw_data = raw_data
        client.client_request_id = None

        json_data = client.get_one(
            self.chift_vertical,
            self.chift_model,
            chift_id=chift_id,
            extra_path=self.extra_path,
            params=params,
        )
        if raw_data:
            if map_model:
                return ObjectWithRawData[T](
                    chift_data=self.model(**json_data),
                    raw_data=json_data.get("raw_data") or {},
                )
            else:
                return json_data
        return self.model(**json_data) if map_model else json_data


class CreateMixin(BaseMixin, Generic[T]):
    @overload
    def create(
        self,
        data,
        client=None,
        params=None,
        map_model: Literal[True] = True,
        client_request_id=None,
    ) -> T: ...

    @overload
    def create(
        self,
        data,
        client=None,
        params=None,
        map_model: Literal[False] = False,
        client_request_id=None,
    ) -> dict: ...

    def create(
        self, data, client=None, params=None, map_model=True, client_request_id=None
    ) -> T | dict:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id
        client.raw_data = False
        client.client_request_id = client_request_id

        json_data = client.post_one(
            self.chift_vertical,
            self.chift_model_create,
            data,
            extra_path=self.extra_path,
            params=params,
        )

        return self.model(**json_data) if map_model else json_data


class UpdateMixin(BaseMixin, Generic[T]):
    @overload
    def update(
        self,
        chift_id,
        data,
        client=None,
        params=None,
        map_model: Literal[True] = True,
        client_request_id=None,
    ) -> T: ...

    @overload
    def update(
        self,
        chift_id,
        data,
        client=None,
        params=None,
        map_model: Literal[False] = False,
        client_request_id=None,
    ) -> dict: ...

    def update(
        self,
        chift_id,
        data,
        client=None,
        params=None,
        map_model=True,
        client_request_id=None,
    ) -> T | dict:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id
        client.raw_data = False
        client.client_request_id = client_request_id

        json_data = client.update_one(
            self.chift_vertical,
            self.chift_model,
            chift_id,
            data,
            extra_path=self.extra_path,
            params=params,
        )

        return self.model(**json_data) if map_model else json_data


class PaginationMixin(BaseMixin, Generic[T]):
    def __iter_page(
        self,
        params=None,
        client=None,
        limit=None,
        raw_data=False,
    ) -> Generator[dict, Any, None]:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id
        client.raw_data = raw_data
        client.client_request_id = None

        if not params:
            params = {}

        size = limit if limit and limit < 100 else 100

        page = 1
        count = 0

        while True:
            json_data = client.get_all(
                self.chift_vertical,
                self.chift_model,
                params={"page": page, "size": size} | params,
                extra_path=self.extra_path,
            )
            yield json_data
            page += 1
            count += len(json_data.get("items", []))
            total = json_data.get("total", 0)
            if (count >= total or not json_data.get("items")) or (
                limit and count >= limit
            ):
                break

    @overload
    def all(
        self,
        params=None,
        client=None,
        map_model: Literal[True] = True,
        limit=None,
        raw_data: Literal[False] = False,
    ) -> list[T]: ...

    @overload
    def all(
        self,
        params=None,
        client=None,
        map_model: Literal[False] = False,
        limit=None,
        raw_data: Literal[False] = False,
    ) -> list[dict]: ...

    @overload
    def all(
        self,
        params=None,
        client=None,
        map_model=False,
        limit=False,
        raw_data: Literal[True] = True,
    ) -> dict: ...

    def all(
        self, params=None, client=None, map_model=True, limit=None, raw_data=False
    ) -> list[T | dict] | dict:
        all_items = []
        for page in self.__iter_page(
            params=params,
            client=client,
            limit=limit,
            raw_data=raw_data,
        ):
            if raw_data:
                return page.get("raw_data") or {}
            all_items.extend(
                self.model(**item) if map_model else item
                for item in page.get("items", [])
            )
        return all_items

    @overload
    def iter_all(
        self,
        params=None,
        client=None,
        map_model: Literal[True] = True,
        limit=None,
    ) -> Generator[T, Any, None]: ...

    @overload
    def iter_all(
        self,
        params=None,
        client=None,
        map_model: Literal[False] = False,
        limit=None,
    ) -> Generator[dict, Any, None]: ...

    def iter_all(
        self,
        params=None,
        client=None,
        map_model=True,
        limit=None,
    ) -> Generator[T | dict, Any, None]:
        for page in self.__iter_page(
            params=params,
            client=client,
            limit=limit,
            raw_data=False,
        ):
            for item in page.get("items", []):
                if map_model:
                    yield self.model(**item)
                else:
                    yield item


class ListMixin(BaseMixin, Generic[T]):
    def all(self, params=None, client=None) -> list[T]:
        if not client:
            client = ChiftClient()
        client.consumer_id = self.consumer_id
        client.connection_id = self.connection_id
        client.raw_data = False
        client.client_request_id = None

        json_data = client.get_all(
            self.chift_vertical,
            self.chift_model,
            params=params,
            extra_path=self.extra_path,
        )

        return [self.model(**item) for item in json_data]
