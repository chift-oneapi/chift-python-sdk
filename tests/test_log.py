import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


@pytest.mark.mock_chift_response(
    ChiftException("The chainexecutionid needs to be passed in the headers")
)
def test_log(two_connections_consumer: Consumer):
    consumer = two_connections_consumer

    # will raise if no connectionid is set
    with pytest.raises(ChiftException) as e:
        consumer.Log.create(
            [
                {
                    "logid": "1",
                    "type": "INFO",
                    "message": "ok",
                    "when": "2023-01-01 01:01:01",
                }
            ]
        )

    assert e.value.message == "The chainexecutionid needs to be passed in the headers"
