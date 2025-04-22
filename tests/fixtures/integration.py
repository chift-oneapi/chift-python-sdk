import uuid

INTEGRATIONS_ALL = [
    {
        "integrationid": 1,
        "name": "Evoliz",
        "status": "active",
        "api": "Accounting",
        "logo_url": "https://example.com/logo/evoliz.png",
        "icon_url": "https://example.com/icon/evoliz.png",
        "post_connections": [],
        "credentials": [],
    },
    {
        "integrationid": 2,
        "name": "QuickBooks",
        "status": "active",
        "api": "Accounting",
        "logo_url": "https://example.com/logo/quickbooks.png",
        "icon_url": "https://example.com/icon/quickbooks.png",
        "post_connections": [],
        "credentials": [],
    },
    {
        "integrationid": 3,
        "name": "Stripe",
        "status": "active",
        "api": "Payment",
        "logo_url": "https://example.com/logo/stripe.png",
        "icon_url": "https://example.com/icon/stripe.png",
        "post_connections": [],
        "credentials": [],
    },
]

INTEGRATION_GET = {
    "integrationid": 1,
    "name": "Evoliz",
    "status": "active",
    "api": "Accounting",
    "logo_url": "https://example.com/logo/evoliz.png",
    "icon_url": "https://example.com/icon/evoliz.png",
    "post_connections": [],
    "credentials": [],
}

SYNCS_ALL = {
    "items": [
        {
            "name": "E-commerce to Accounting",
            "connections": [
                {
                    "one_api": 1,
                    "connection_type": None,
                    "display_order": 0,
                    "display_hidden": False,
                },
                {
                    "one_api": 2,
                    "connection_type": None,
                    "display_order": 1,
                    "display_hidden": False,
                },
            ],
            "syncid": str(uuid.uuid4()),
            "consumers": [],
            "flows": [
                {
                    "name": "Sync Orders",
                    "id": str(uuid.uuid4()),
                    "execution": {"type": "code", "data": {"code": "# Code here"}},
                }
            ],
        },
        {
            "name": "POS to Accounting",
            "connections": [
                {
                    "one_api": 3,
                    "connection_type": None,
                    "display_order": 0,
                    "display_hidden": False,
                },
                {
                    "one_api": 1,
                    "connection_type": None,
                    "display_order": 1,
                    "display_hidden": False,
                },
            ],
            "syncid": str(uuid.uuid4()),
            "consumers": [],
            "flows": [
                {
                    "name": "Sync Sales",
                    "id": str(uuid.uuid4()),
                    "execution": {"type": "code", "data": {"code": "# Code here"}},
                }
            ],
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}
