import uuid

WEBHOOK_ALL = [
    {
        "webhookid": uuid.uuid4(),
        "accountid": uuid.uuid4(),
        "createdby": uuid.uuid4(),
        "createdon": "2025-04-20T14:30:00Z",
        "event": "user.created",
        "url": "https://example.com/webhooks/user.created",
        "status": "active",
        "integrationid": 1001,
    },
    {
        "webhookid": uuid.uuid4(),
        "accountid": uuid.uuid4(),
        "createdby": None,
        "createdon": "2025-04-21T09:15:00Z",
        "event": "order.updated",
        "url": "https://example.com/webhooks/order.updated",
        "status": "active",
        "integrationid": None,
    },
    {
        "webhookid": uuid.uuid4(),
        "accountid": uuid.uuid4(),
        "createdby": uuid.uuid4(),
        "createdon": "2025-04-22T08:00:00Z",
        "event": "payment.failed",
        "url": "https://example.com/webhooks/payment.failed",
        "status": "inactive",
        "integrationid": 1002,
    },
]

WEBHOOK_TYPES_ALL = [
    {
        "event": "user.created",
        "api": "v1/users/create",
    },
    {
        "event": "order.placed",
        "api": None,
    },
    {
        "event": "invoice.paid",
        "api": "v1/invoices/paid",
    },
]
