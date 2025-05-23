import uuid
from datetime import datetime

import pytest

from chift.openapi.models import Sync
from tests.fixtures import sync

today_date = datetime.now().strftime("%d/%m/%Y")


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
        "triggers": [{"id": "trigger-1", "type": trigger_type}],
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

    if trigger_type == "timer":
        data["triggers"][0]["cronschedules"] = ["0/30 * * * *"]

    if execution_type == "code":
        data["execution"]["data"]["code"] = "console.log('This is fucking awesome!')"

    if execution_type == "module":
        data["execution"]["data"]["name"] = "Invoice to invoice"

    return data


def get_sync(chift):
    # TODO: improve this once sync creation endpoint is there
    sync = chift.Sync.get("76d8b868-4900-4302-9eee-c3d62bb79b2d")
    return sync


@pytest.mark.mock_chift_response(sync.READ_SYNC_ALL, sync.READ_SYNC_ALL[0])
def test_sync(chift):
    syncs = chift.Sync.all()

    assert syncs

    expected_sync = syncs[0]

    actual_sync = chift.Sync.get(expected_sync.syncid)

    assert expected_sync.name == actual_sync.name


@pytest.mark.skip(
    reason="The test is too complex for unit testing. it should be split into smaller tests."
)
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


@pytest.mark.skip(
    reason="The test is too complex for unit testing. it should be split into smaller tests."
)
def test_flow_create_trigger_code(chift):
    syncs = chift.Sync.all()

    sync: Sync = syncs[0]

    # create flow
    flow_created = chift.Flow.create(sync.syncid, _get_flow_data(execution_type="code"))

    # test trigger flow of type code (AWS lambda) should not raise
    chift.Flow.trigger(
        sync.syncid, flow_created.id, {"data": {"from_date": today_date}}
    )


@pytest.mark.skip(
    reason="The test is too complex for unit testing. it should be split into smaller tests."
)
def test_flow_create_trigger_module(chift):
    syncs = chift.Sync.all()
    sync: Sync = syncs[0]

    # create flow
    flow_created = chift.Flow.create(
        sync.syncid, _get_flow_data(execution_type="module")
    )

    # test trigger flow of type chain should not raise
    chift.Flow.trigger(
        sync.syncid, flow_created.id, {"data": {"from_date": today_date}}
    )


@pytest.mark.skip(
    reason="The test is too complex for unit testing. it should be split into smaller tests."
)
def test_flow_create_trigger_timer(chift):
    syncs = chift.Sync.all()

    sync: Sync = syncs[0]

    # create flow with timer should not raise
    flow_created = chift.Flow.create(sync.syncid, _get_flow_data(trigger_type="timer"))

    assert flow_created


@pytest.mark.skip(
    reason="The test is too complex for unit testing. it should be split into smaller tests."
)
def test_create_flow(chift):
    sync = get_sync(chift)

    datastore_name = str(uuid.uuid1())
    data = _get_flow_data(
        flow_name="Migration de factures",
        datastore_name=datastore_name,
        execution_type="module",
    )
    flow_created = chift.Flow.create(sync.syncid, data)

    assert flow_created.id in [flow.id for flow in chift.Sync.get(sync.syncid).flows]

    # let's trigger it
    res = chift.Flow.trigger(
        sync.syncid,
        flow_created.id,
        {"data": {"from_date": today_date}},
    )
    status = chift.Flow.chainexecution(
        sync.syncid, flow_created.id, res["data"]["executionid"]
    )
    assert status.get("status")

    # let's trigger it for one consumer
    chift.Flow.trigger(
        sync.syncid,
        flow_created.id,
        {"consumers": sync.consumers[:1], "data": {"from_date": today_date}},
    )

    # test getting sync for consumer info
    consumer = chift.Consumer.get(sync.consumers[0])
    info = consumer.Sync.get(sync.syncid)
    assert info


@pytest.mark.skip(
    reason="The test is too complex for unit testing. it should be split into smaller tests."
)
def test_datastore(chift):
    sync = get_sync(chift)

    consumer = chift.Consumer.get(sync.consumers[0])
    datastore = sync.flows[0].config.datastores[0]

    # test create
    value = {}

    str_column_name = None

    for column in datastore.definition.columns:
        if column.type == "json":
            value[column.name] = {"1": "1"}
        elif column.type == "number":
            value[column.name] = 1
        else:
            str_column_name = column.name
            value[column.name] = "1"

    data = consumer.Data.create(datastore.id, [{"data": value}])[0]

    # test update
    updated_value = data.data
    if str_column_name in updated_value:
        updated_value[str_column_name] = "2"

    updated_data = consumer.Data.update(datastore.id, data.id, {"data": updated_value})

    if str_column_name in updated_data.data:
        assert updated_data.data[str_column_name] == "2"
