def test_datastore(chift):
    datastores = chift.Datastore.all()

    assert datastores

    for datastore in datastores:
        assert datastore.name and datastore.definition
