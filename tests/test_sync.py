import uuid

from chift.openapi.models import Sync


def _get_flow_data(
    flow_name=None, datastore_name=None, trigger_type="event", execution_type="code"
):
    if not flow_name:
        flow_name = str(uuid.uuid1())
    if not datastore_name:
        datastore_name = str(uuid.uuid1())

    data = {
        "name": flow_name,
        "description": "test",
        "trigger": {"type": trigger_type, "data": {}},
        "execution": {
            "type": execution_type,
            "data": {},
        },
        "config": {
            "datastores": [
                {
                    "name": "INVOICES",
                    "definition": {
                        "columns": [
                            {
                                "name": "source_id",
                                "type": "text",
                                "title": "Invoice source id",
                            },
                            {
                                "name": "target_id",
                                "type": "text",
                                "title": "Invoice target id",
                            },
                            {
                                "name": "reference",
                                "type": "text",
                                "title": "Invoice code/ref",
                            },
                        ],
                        "search_column": "source_id",
                    },
                },
                {
                    "name": "CONTACTS",
                    "definition": {
                        "columns": [
                            {
                                "name": "source_id",
                                "type": "text",
                                "title": "Contact source id",
                            },
                            {
                                "name": "target_id",
                                "type": "text",
                                "title": "Contact target id",
                            },
                        ],
                        "search_column": "source_id",
                    },
                },
                {
                    "name": "PRODUCTS",
                    "definition": {
                        "columns": [
                            {
                                "name": "source_id",
                                "type": "text",
                                "title": "Product source id",
                            },
                            {
                                "name": "target_id",
                                "type": "text",
                                "title": "Product target id",
                            },
                            {
                                "name": "reference",
                                "type": "text",
                                "title": "Product code/ref",
                            },
                        ],
                        "search_column": "source_id",
                    },
                },
                {
                    "name": "ERRORS",
                    "definition": {
                        "columns": [
                            {
                                "name": "message",
                                "type": "text",
                                "title": "Error message",
                            },
                            {
                                "name": "source_id",
                                "type": "text",
                                "title": "Invoice source id",
                            },
                        ]
                    },
                },
            ],
            "definitionFields": [
                {
                    "type": "date",
                    "title": "Début de la synchronisation? (dd/mm/yyyy)",
                    "name": "from_date",
                    "optional": False,
                },
                {
                    "type": "text",
                    "title": "Valeur par défault pour le pays (ISO2)",
                    "name": "default_country",
                    "default": "FR",
                    "optional": True,
                },
            ],
            "customFields": [
                {
                    "type": "source_node_id",
                    "value": 7012,
                },
                {
                    "type": "target_node_id",
                    "value": 7010,
                },
                {
                    "type": "tax_mapping_name",
                    "value": "Tax Rates Mapping",
                },
            ],
        },
    }

    if trigger_type == "time":
        data["trigger"]["data"]["cronschedule"] = "0/30 * * * *"

    if execution_type == "code":
        data["execution"]["data"]["code"] = "console.log('This is fucking awesome!')"

    if execution_type == "chain":
        data["execution"]["data"]["name"] = "Invoice to invoice"

    return data


def test_sync(chift):
    syncs = chift.Sync.all()

    assert syncs

    expected_sync = syncs[0]

    actual_sync = chift.Sync.get(expected_sync.syncid)

    assert expected_sync == actual_sync


def test_flow_update(chift):
    syncs = chift.Sync.all()

    sync: Sync = syncs[0]

    # create flow
    datastore_name = str(uuid.uuid1())
    data = _get_flow_data(datastore_name=datastore_name)
    flow_created = chift.Flow.create(sync.syncid, data)

    assert flow_created.id in [flow.id for flow in chift.Sync.get(sync.syncid).flows]

    # update flow
    data["description"] = "test updated"
    data["config"]["datastores"] = [
        {
            "name": datastore_name,
            "definition": {
                "columns": [{"name": "test_x", "title": "title", "type": "text"}]
            },
        },
        {
            "name": str(uuid.uuid1()),
            "definition": {
                "columns": [{"name": "test_y", "title": "title", "type": "text"}]
            },
        },
    ]
    flow_updated = chift.Flow.create(sync.syncid, data)

    assert flow_updated.id == flow_created.id

    for flow in chift.Sync.get(sync.syncid).flows:
        if flow.id == flow_created.id:
            assert flow.description == "test updated"
            assert len(flow.config.datastores) == 2

    chift.Flow.delete(sync.syncid, flow_created.id)


def test_flow_execution_code(chift):
    syncs = chift.Sync.all()

    sync: Sync = syncs[0]

    # create flow
    flow_created = chift.Flow.create(sync.syncid, _get_flow_data(execution_type="code"))

    # test trigger flow of type cde (AWS lambda) should not raise
    chift.Flow.trigger(sync.syncid, flow_created.id, {})


def test_flow_execution_chain(chift):
    syncs = chift.Sync.all()

    sync: Sync = syncs[0]

    # create flow
    flow_created = chift.Flow.create(
        sync.syncid, _get_flow_data(execution_type="chain")
    )

    # test trigger flow of type chain should not raise
    chift.Flow.trigger(sync.syncid, flow_created.id, {})


def test_flow_trigger_timer(chift):
    syncs = chift.Sync.all()

    sync: Sync = syncs[0]

    # create flow with timer should not raise
    flow_created = chift.Flow.create(sync.syncid, _get_flow_data(trigger_type="timer"))

    assert flow_created


def test_create_flow(chift, sync):
    datastore_name = str(uuid.uuid1())
    data = _get_flow_data(
        flow_name="Migration de factures",
        datastore_name=datastore_name,
        execution_type="chain",
    )
    flow_created = chift.Flow.create(sync.syncid, data)

    assert flow_created.id in [flow.id for flow in chift.Sync.get(sync.syncid).flows]


def test_trigger_flows(chift, sync):
    for flow in sync.flows[:2]:  # test only two
        res = chift.Flow.trigger(
            sync.syncid,
            flow.id,
            {},
        )
        status = chift.Flow.chainexecution(
            sync.syncid, flow.id, res["data"]["executionid"]
        )
        assert status.get("status")


def test_trigger_flows_for_consumer(chift, sync):
    for flow in sync.flows[:2]:  # test only two
        chift.Flow.trigger(
            sync.syncid,
            flow.id,
            {"consumers": sync.consumers[:1]},
        )
        # test getting sync for consumer info
        consumer = chift.Consumer.get(sync.consumers[0])
        info = consumer.sync.Sync.get(sync.syncid)
        assert info
