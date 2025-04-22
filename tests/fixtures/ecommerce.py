CUSTOMER_ALL = {
    "items": [
        {
            "id": "client-001",
            "source_ref": {"id": "c-001", "model": "customer"},
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+123456789",
            "email": "john.doe@example.com",
            "language": "en",
            "internal_notes": None,
            "currency": "USD",
            "addresses": [
                {
                    "address_type": "main",
                    "company_name": None,
                    "first_name": "John",
                    "last_name": "Doe",
                    "street": "123 Elm St",
                    "number": "1",
                    "box": None,
                    "city": "Springfield",
                    "postal_code": "12345",
                    "country": "US",
                    "phone": None,
                    "email": None,
                }
            ],
            "created_on": "2025-01-01T12:00:00Z",
        },
        {
            "id": "client-002",
            "source_ref": {"id": "c-002", "model": "customer"},
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "+1987654321",
            "email": "jane.smith@example.com",
            "language": "en",
            "internal_notes": None,
            "currency": "EUR",
            "addresses": [
                {
                    "address_type": "main",
                    "company_name": None,
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "street": "456 Oak Ave",
                    "number": "2",
                    "box": None,
                    "city": "Amsterdam",
                    "postal_code": "1011AB",
                    "country": "NL",
                    "phone": None,
                    "email": None,
                }
            ],
            "created_on": "2025-01-02T09:30:00Z",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}
PRODUCT_ALL = {
    "items": [
        {
            "id": "product-001",
            "source_ref": {"id": "p-001", "model": "product"},
            "name": "T-Shirt",
            "description": "Classic cotton t-shirt",
            "description_html": None,
            "categories": [],
            "created_on": "2025-01-05T14:00:00Z",
            "variants": [
                {
                    "id": "variant-001",
                    "source_ref": {"id": "v-001", "model": "variant"},
                    "parent_id": "product-001",
                    "name": "T-Shirt Size M",
                    "available_quantity": 25,
                }
            ],
            "status": None,
            "common_attributes": [],
            "variant_attributes_options": [],
            "common_images": [],
        },
        {
            "id": "product-002",
            "source_ref": {"id": "p-002", "model": "product"},
            "name": "Mug",
            "description": "Ceramic coffee mug",
            "description_html": None,
            "categories": [],
            "created_on": "2025-01-06T10:15:00Z",
            "variants": [
                {
                    "id": "variant-002",
                    "source_ref": {"id": "v-002", "model": "variant"},
                    "parent_id": "product-002",
                    "name": "Mug Standard",
                    "available_quantity": 0,
                }
            ],
            "status": None,
            "common_attributes": [],
            "variant_attributes_options": [],
            "common_images": [],
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

LOCATION_ALL = {
    "items": [
        {
            "id": "location-001",
            "name": "Warehouse A",
            "source_ref": {"id": "l-001", "model": "location"},
        },
        {
            "id": "location-002",
            "name": "Store B",
            "source_ref": {"id": "l-002", "model": "location"},
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

PAYMENT_METHOD_ALL = {
    "items": [
        {
            "id": "pm-001",
            "source_ref": {"id": "pm-001", "model": "payment_method"},
            "name": "Credit Card",
            "active": True,
        },
        {
            "id": "pm-002",
            "source_ref": {"id": "pm-002", "model": "payment_method"},
            "name": "PayPal",
            "active": True,
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
            "source_ref": {"id": "cat-001", "model": "category"},
            "name": "Apparel",
            # "parent_id": None  # можно добавить, если нужно
        },
        {
            "id": "cat-002",
            "source_ref": {"id": "cat-002", "model": "category"},
            "name": "Home Goods",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

TAX_ALL = {
    "items": [
        {
            "id": "tax-001",
            "source_ref": {"id": "tax-001", "model": "tax"},
            "label": "VAT 21%",
            "rate": 0.21,
            "country": None,
        },
        {
            "id": "tax-002",
            "source_ref": {"id": "tax-002", "model": "tax"},
            "label": "Reduced VAT 10%",
            "rate": 0.10,
            "country": None,
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
            "status": "confirmed",
            "discount_amount": 0.0,
            "untaxed_amount_without_fees": 49.99,
            "tax_amount_without_fees": 9.99,
            "total_without_fees": 59.98,
            "current_untaxed_amount": 49.99,
            "current_tax_amount": 9.99,
            "current_total": 59.98,
            "untaxed_amount": 49.99,
            "tax_amount": 9.99,
            "total": 59.98,
            "currency": "USD",
            "lines": [
                {
                    "id": "line-001",
                    "source_ref": {"id": "ol-001", "model": "order_line"},
                    "quantity": 1,
                    "current_quantity": 1,
                    "unit_price": 49.99,
                    "description": "T-Shirt",
                    "tax_rate": 20.0,
                    "untaxed_amount": 49.99,
                    "tax_amount": 9.99,
                    "total": 59.98,
                }
            ],
        },
        {
            "id": "order-002",
            "source_ref": {"id": "o-002", "model": "order"},
            "status": "confirmed",
            "discount_amount": 0.0,
            "untaxed_amount_without_fees": 19.99,
            "tax_amount_without_fees": 3.99,
            "total_without_fees": 23.98,
            "current_untaxed_amount": 19.99,
            "current_tax_amount": 3.99,
            "current_total": 23.98,
            "untaxed_amount": 19.99,
            "tax_amount": 3.99,
            "total": 23.98,
            "currency": "EUR",
            "lines": [
                {
                    "id": "line-002",
                    "source_ref": {"id": "ol-002", "model": "order_line"},
                    "quantity": 1,
                    "current_quantity": 1,
                    "unit_price": 19.99,
                    "description": "Mug",
                    "tax_rate": 20.0,
                    "untaxed_amount": 19.99,
                    "tax_amount": 3.99,
                    "total": 23.98,
                }
            ],
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}
