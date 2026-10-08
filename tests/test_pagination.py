from typing import ClassVar, Generator

import pytest
from pydantic import BaseModel

from chift.api.client import ChiftClient
from chift.api.mixins import PaginationMixin
from tests.fixtures import pagination


class PaginationTestModel(BaseModel):
    id: int


class PaginationTest(PaginationMixin[PaginationTestModel]):
    chift_vertical: ClassVar = "TESTING"
    chift_model: ClassVar = "TESTING"
    model = PaginationTestModel


@pytest.fixture
def pagination_router(test_consumer):
    return PaginationTest(test_consumer.consumerid, None)


@pytest.mark.mock_chift_response(pagination.PAGINATION_MANY_DATA)
def test_pagination_all(pagination_router: PaginationTest):
    assert pagination_router.all(map_model=True) == [
        PaginationTestModel(id=_id) for _id in range(0, 150)
    ]


@pytest.mark.mock_chift_response(pagination.PAGINATION_MANY_DATA)
def test_pagination_all_no_map(pagination_router: PaginationTest):
    assert pagination_router.all(map_model=False) == [
        {"id": _id} for _id in range(0, 150)
    ]


@pytest.mark.mock_chift_response(pagination.PAGINATION_MANY_DATA)
def test_pagination_iter_all(pagination_router: PaginationTest):
    generator = pagination_router.iter_all(map_model=True)
    assert isinstance(generator, Generator)
    for _id, instance in zip(range(0, 150), generator):
        assert instance == PaginationTestModel(id=_id)


@pytest.mark.mock_chift_response(pagination.PAGINATION_MANY_DATA)
def test_pagination_iter_all_no_map(pagination_router: PaginationTest):
    generator = pagination_router.iter_all(map_model=False)
    assert isinstance(generator, Generator)
    for _id, instance in zip(range(0, 150), generator):
        assert instance == {"id": _id}


@pytest.fixture
def requested_sizes(monkeypatch):
    sizes = []

    def fake_make_request(self, method, path, params=None, **kwargs):
        sizes.append(params["size"])
        start = (params["page"] - 1) * params["size"]
        items = [{"id": _id} for _id in range(start, min(start + params["size"], 150))]
        return {"total": 150, "items": items}

    monkeypatch.setattr(ChiftClient, "make_request", fake_make_request)
    return sizes


def test_pagination_default_page_size(
    pagination_router: PaginationTest, requested_sizes
):
    assert len(pagination_router.all(map_model=False)) == 150
    assert requested_sizes == [100, 100]


def test_pagination_page_size(pagination_router: PaginationTest, requested_sizes):
    assert len(list(pagination_router.iter_all(map_model=False, page_size=1000))) == 150
    assert requested_sizes == [1000]


def test_pagination_limit_below_page_size(
    pagination_router: PaginationTest, requested_sizes
):
    assert len(pagination_router.all(map_model=False, limit=30, page_size=1000)) == 30
    assert requested_sizes == [30]


def test_invoice_iter_all_forwards_page_size(test_consumer, monkeypatch):
    sizes = []

    def fake_make_request(self, method, path, params=None, **kwargs):
        sizes.append(params["size"])
        return {"total": 0, "items": []}

    monkeypatch.setattr(ChiftClient, "make_request", fake_make_request)

    list(test_consumer.accounting.Invoice.iter_all("customer_invoice", page_size=1000))

    assert sizes == [1000]
