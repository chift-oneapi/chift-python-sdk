import pytest

from chift.api.exceptions import ChiftException
from chift.openapi.models import Consumer


def test_log(evoliz_consumer: Consumer):
    consumer = evoliz_consumer

    # will raise if no connectionid is set
    with pytest.raises(ChiftException) as e:
        consumer.log.Logs.create(
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
