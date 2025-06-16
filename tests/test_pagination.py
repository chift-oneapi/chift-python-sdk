from typing import ClassVar, Generator

import pytest
from pydantic import BaseModel

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
