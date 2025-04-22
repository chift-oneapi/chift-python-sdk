CUSTOMER_ALL = {
    "items": [
        {
            "id": "cust-001",
            "first_name": "Alice",
            "last_name": "Johnson",
            "name": "Alice Johnson",
            "phone": "+10000000001",
            "email": "alice.johnson@example.com",
            "created_on": "2025-01-10T09:00:00Z",
            "addresses": [],
        },
        {
            "id": "cust-002",
            "first_name": "Bob",
            "last_name": "Smith",
            "name": "Bob Smith",
            "phone": "+10000000002",
            "email": "bob.smith@example.com",
            "created_on": "2025-01-11T10:30:00Z",
            "addresses": [],
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

CUSTOMER_CREATE = {
    "id": "cust-test-123",
    "source_ref": {"id": "c-test-123", "model": "customer"},
    "first_name": "Test",
    "last_name": "Customer",
    "name": "Test Customer",
    "email": "test.customer@example.com",
    "phone": None,
    "created_on": "2025-01-20T12:00:00Z",
    "addresses": [],
}

CUSTOMER_GET = {
    "id": "cust-test-123",
    "source_ref": {"id": "c-test-123", "model": "customer"},
    "first_name": "Test",
    "last_name": "Customer",
    "name": "Test Customer",
    "email": "test.customer@example.com",
    "phone": None,
    "created_on": "2025-01-20T12:00:00Z",
    "addresses": [],
}

PAYMENT_METHODS_ALL = {
    "items": [
        {
            "id": "pm-001",
            "source_ref": {"id": "pm-001", "model": "payment_method"},
            "name": "Cash",
            "extra": "Cash Payment",
        },
        {
            "id": "pm-002",
            "source_ref": {"id": "pm-002", "model": "payment_method"},
            "name": "Card",
            "extra": "Credit/Debit Card Payment",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}


SALES_ITEM = {
    "total": 250.0,
    "tax_amount": 41.67,
    "taxes": [{"tax_rate": 20.0, "tax_amount": 41.67, "total": 250.0}],
}

LOCATION_ALL = {
    "items": [
        {
            "id": "loc-001",
            "name": "Store 1",
            "timezone": "America/New_York",
            "address": {
                "address_type": "main",
                "street": "123 Main Street",
                "city": "New York",
                "postal_code": "10001",
                "country": "US",
            },
        },
        {
            "id": "loc-002",
            "name": "Store 2",
            "timezone": "America/Los_Angeles",
            "address": {
                "address_type": "main",
                "street": "456 Market Street",
                "city": "San Francisco",
                "postal_code": "94103",
                "country": "US",
            },
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

ORDER_ALL = {
    "items": [
        {
            "id": "order-001",
            "source_ref": {"id": "o-001", "model": "order"},
            "creation_date": "2025-01-15T14:30:00Z",
            "total": 120.0,
            "tax_amount": 20.0,
            "items": [
                {
                    "id": "line-001",
                    "source_ref": {"id": "ol-001", "model": "order_line"},
                    "quantity": 2,
                    "unit_price": 50.0,
                    "total": 120.0,
                    "tax_amount": 20.0,
                    "description": "Coffee Small",
                    "tax_rate": 20.0,
                    "product_id": "var-001",
                }
            ],
            "payments": [
                {
                    "payment_method_id": "pm-001",
                    "payment_method_name": "Cash",
                    "total": 120.0,
                    "date": "2025-01-15T14:35:00Z",
                }
            ],
        },
        {
            "id": "order-002",
            "source_ref": {"id": "o-002", "model": "order"},
            "creation_date": "2025-01-16T10:15:00Z",
            "total": 114.0,
            "tax_amount": 19.0,
            "items": [
                {
                    "id": "line-002",
                    "source_ref": {"id": "ol-002", "model": "order_line"},
                    "quantity": 1,
                    "unit_price": 95.0,
                    "total": 114.0,
                    "tax_amount": 19.0,
                    "description": "Tea Large",
                    "tax_rate": 20.0,
                    "product_id": "var-002",
                }
            ],
            "payments": [
                {
                    "payment_method_id": "pm-002",
                    "payment_method_name": "Card",
                    "total": 114.0,
                    "date": "2025-01-16T10:20:00Z",
                }
            ],
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

CLOSURE = {
    "date": "2025-01-14",
    "status": "closed",
    "closures": [
        {
            "id": "closure-001",
            "total": 234.0,
            "tax_amount": 39.0,
            "payments": [
                {
                    "payment_method_id": "pm-001",
                    "payment_method_name": "Cash",
                    "total": 120.0,
                },
                {
                    "payment_method_id": "pm-002",
                    "payment_method_name": "Card",
                    "total": 114.0,
                },
            ],
            "taxes": [{"tax_rate": 20.0, "tax_amount": 39.0, "total": 234.0}],
        }
    ],
}

PRODUCT_ALL = {
    "items": [
        {
            "id": "prod-001",
            "categories": ["cat-001"],
            "name": "Coffee",
            "description": "Freshly brewed coffee",
            "prices": [{"unit_price": 1.75, "tax_rate": 20.0}],
            "accounting_category_ids": ["acc-cat-001"],
        },
        {
            "id": "prod-002",
            "categories": ["cat-001"],
            "name": "Tea",
            "description": "Green tea",
            "prices": [{"unit_price": 1.95, "tax_rate": 20.0}],
            "accounting_category_ids": ["acc-cat-001"],
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

PRODUCT_CATEGORY_ALL = {
    "items": [
        {
            "id": "cat-001",
            "name": "Beverages",
            "description": "All drink items",
            "id_parent": None,
        }
    ],
    "total": 1,
    "page": 1,
    "size": 10,
}

PAYMENT_METHOD_ALL = {
    "items": [
        {
            "id": "pm-001",
            "source_ref": {"id": "pm-001", "model": "payment_method"},
            "name": "Cash",
        },
        {
            "id": "pm-002",
            "source_ref": {"id": "pm-002", "model": "payment_method"},
            "name": "Card",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}
PAYMENT_ALL = {
    "items": [
        {
            "id": "pay-001",
            "payment_method_id": "pm-001",
            "payment_method_name": "Cash",
            "total": 120.0,
            "tip": 5.0,
            "status": "Completed",
            "currency": "USD",
            "date": "2025-01-15T14:35:00Z",
        },
        {
            "id": "pay-002",
            "payment_method_id": "pm-002",
            "payment_method_name": "Card",
            "total": 114.0,
            "tip": 0.0,
            "status": "Completed",
            "currency": "USD",
            "date": "2025-01-16T10:20:00Z",
        },
        {
            "id": "pay-003",
            "payment_method_id": "pm-002",
            "payment_method_name": "Card",
            "total": 85.50,
            "tip": 10.0,
            "status": "Completed",
            "currency": "USD",
            "date": "2025-01-16T15:45:00Z",
        },
        {
            "id": "pay-004",
            "payment_method_id": "pm-001",
            "payment_method_name": "Cash",
            "total": 23.75,
            "tip": 2.25,
            "status": "Completed",
            "currency": "USD",
            "date": "2025-01-17T09:10:00Z",
        },
        {
            "id": "pay-005",
            "payment_method_id": "pm-002",
            "payment_method_name": "Card",
            "total": 42.0,
            "tip": 0.0,
            "status": "Pending",
            "currency": "USD",
            "date": "2025-01-17T11:30:00Z",
        },
    ],
    "total": 5,
    "page": 1,
    "size": 10,
}
