import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


def test_log(invoicing_consumer: Consumer):
    consumer = invoicing_consumer

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
