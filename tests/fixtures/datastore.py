import uuid

DATASTORE_ALL = [
    {
        "id": str(uuid.uuid4()),
        "name": "Customer Datastore",
        "status": "active",
        "definition": {
            "columns": [
                {
                    "name": "customer_id",
                    "title": "Customer ID",
                    "type": "string",
                    "optional": False,
                },
                {
                    "name": "customer_name",
                    "title": "Customer Name",
                    "type": "string",
                    "optional": False,
                },
                {"name": "email", "title": "Email", "type": "string", "optional": True},
            ],
            "search_column": "customer_name",
        },
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Invoice Datastore",
        "status": "active",
        "definition": {
            "columns": [
                {
                    "name": "invoice_id",
                    "title": "Invoice ID",
                    "type": "string",
                    "optional": False,
                },
                {
                    "name": "invoice_date",
                    "title": "Invoice Date",
                    "type": "date",
                    "optional": False,
                },
                {
                    "name": "total_amount",
                    "title": "Total Amount",
                    "type": "number",
                    "optional": False,
                },
                {
                    "name": "customer_id",
                    "title": "Customer ID",
                    "type": "string",
                    "optional": False,
                },
            ],
            "search_column": "invoice_id",
        },
    },
]
DATASTORE_GET = {
    "id": str(uuid.uuid4()),
    "name": "Product Datastore",
    "status": "active",
    "definition": {
        "columns": [
            {
                "name": "product_id",
                "title": "Product ID",
                "type": "string",
                "optional": False,
            },
            {
                "name": "product_name",
                "title": "Product Name",
                "type": "string",
                "optional": False,
            },
            {"name": "price", "title": "Price", "type": "number", "optional": False},
            {
                "name": "category",
                "title": "Category",
                "type": "string",
                "optional": True,
            },
        ],
        "search_column": "product_name",
    },
}
