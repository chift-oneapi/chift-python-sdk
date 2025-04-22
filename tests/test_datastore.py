import pytest

from tests.fixtures import datastore


@pytest.mark.mock_chift_response(datastore.DATASTORE_ALL, datastore.DATASTORE_ALL[0])
def test_datastore(chift):
    datastores = chift.Datastore.all()

    assert datastores

    for datastore in datastores:
        assert datastore.name and datastore.definition
