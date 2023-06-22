def test_sync(chift):
    integrations = chift.Integration.all()

    assert integrations

    for integration in integrations:
        assert integration.integrationid
