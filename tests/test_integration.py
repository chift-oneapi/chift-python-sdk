import pytest

from tests.fixtures import integration


@pytest.mark.mock_chift_response(
    integration.INTEGRATIONS_ALL, integration.INTEGRATIONS_ALL[0]
)
def test_sync(chift):
    integrations = chift.Integration.all()

    assert integrations

    for integration in integrations:
        assert integration.integrationid
