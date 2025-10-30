ANALYTIC_PLAN_ALL = {
    "items": [
        {"id": "plan-001", "name": "Default Plan", "active": True},
        {"id": "plan-002", "name": "Marketing Plan", "active": True},
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

TAX_ALL = {
    "items": [
        {
            "id": "tax-001",
            "source_ref": {"id": "t-001", "model": "tax"},
            "label": "VAT 21%",
            "rate": 21.0,
            "type": "sale",
            "code": "VAT21",
            "scope": "nat",
        },
        {
            "id": "tax-002",
            "source_ref": {"id": "t-002", "model": "tax"},
            "label": "VAT 6%",
            "rate": 6.0,
            "type": "sale",
            "code": "VAT6",
            "scope": "nat",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

ACCOUNT_ALL = {
    "items": [
        {"number": "101000", "name": "Cash Account", "active": True, "type": "bank"},
        {
            "number": "400001",
            "name": "Accounts Receivable",
            "active": True,
            "type": "receivable",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

MISCELLANEOUS_OPERATION_ALL = {
    "items": [
        {
            "id": "misc-op-001",
            "operation_number": "MO001",
            "currency": "EUR",
            "currency_exchange_rate": 1.0,
            "lines": [
                {
                    "line_number": 1,
                    "description": "Office supplies",
                    "amount": 100.0,
                    "type": "general_account",
                    "account_number": "610000",
                }
            ],
            "operation_date": "2023-08-01",
            "journal_id": "journal-001",
            "status": "posted",
        },
        {
            "id": "misc-op-002",
            "operation_number": "MO002",
            "currency": "EUR",
            "currency_exchange_rate": 1.0,
            "lines": [
                {
                    "line_number": 1,
                    "description": "Software license",
                    "amount": 299.99,
                    "type": "general_account",
                    "account_number": "611000",
                }
            ],
            "operation_date": "2023-08-15",
            "journal_id": "journal-002",
            "status": "posted",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

CLIENT_ALL = {
    "items": [
        {
            "id": "client-001",
            "name": "Acme Corporation",
            "is_company": True,
            "phone": "+1234567890",
            "email": "contact@acme.com",
            "website": "https://acme.com",
            "currency": "EUR",
            "active": True,
            "addresses": [
                {
                    "address_type": "main",
                    "street": "123 Main St",
                    "city": "Brussels",
                    "postal_code": "1000",
                    "country": "BE",
                }
            ],
            "account_number": "400001",
        },
        {
            "id": "client-002",
            "name": "TechStart Inc.",
            "is_company": True,
            "phone": "+1987654321",
            "email": "info@techstart.com",
            "website": "https://techstart.com",
            "currency": "USD",
            "active": True,
            "addresses": [
                {
                    "address_type": "main",
                    "street": "456 Tech Blvd",
                    "city": "San Francisco",
                    "postal_code": "94107",
                    "country": "US",
                }
            ],
            "account_number": "400002",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

CLIENT_UPDATE = {
    "id": "client-001",
    "name": "Acme Corporation",
    "is_company": True,
    "phone": "+1234567890",
    "email": "contact@acme.com",
    "website": "https://test.com",
    "currency": "EUR",
    "active": True,
    "addresses": [
        {
            "address_type": "main",
            "street": "123 Main St",
            "city": "Brussels",
            "postal_code": "1000",
            "country": "BE",
        }
    ],
    "account_number": "400001",
}

SUPPLIER_ALL = {
    "items": [
        {
            "id": "supplier-001",
            "name": "Office Supplies Co.",
            "is_company": True,
            "phone": "+1234567890",
            "email": "orders@officesupplies.com",
            "website": "https://officesupplies.com",
            "currency": "EUR",
            "active": True,
            "addresses": [
                {
                    "address_type": "main",
                    "street": "789 Supply Road",
                    "city": "Brussels",
                    "postal_code": "1000",
                    "country": "BE",
                }
            ],
            "account_number": "600001",
        },
        {
            "id": "supplier-002",
            "name": "Tech Hardware Ltd",
            "is_company": True,
            "phone": "+1987654321",
            "email": "sales@techhardware.com",
            "website": "https://techhardware.com",
            "currency": "GBP",
            "active": True,
            "addresses": [
                {
                    "address_type": "main",
                    "street": "100 Hardware Ave",
                    "city": "London",
                    "postal_code": "EC1A 1BB",
                    "country": "GB",
                }
            ],
            "account_number": "600002",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

INVOICE_ALL = {
    "items": [
        {
            "id": "invoice-001",
            "invoice_type": "customer_invoice",
            "invoice_number": "INV-2023-001",
            "currency": "EUR",
            "untaxed_amount": 1000.0,
            "tax_amount": 210.0,
            "total": 1210.0,
            "reference": "PO-2023-001",
            "invoice_date": "2023-08-01",
            "due_date": "2023-09-01",
            "partner_id": "client-001",
            "status": "posted",
            "lines": [
                {
                    "line_number": 1,
                    "unit_price": 500.0,
                    "quantity": 2,
                    "untaxed_amount": 1000.0,
                    "tax_rate": 21.0,
                    "tax_amount": 210.0,
                    "total": 1210.0,
                    "account_number": "700000",
                    "tax_code": "tax-001",
                    "description": "Consulting services",
                }
            ],
        },
        {
            "id": "invoice-002",
            "invoice_type": "customer_invoice",
            "invoice_number": "INV-2023-002",
            "currency": "USD",
            "untaxed_amount": 2500.0,
            "tax_amount": 525.0,
            "total": 3025.0,
            "reference": "PO-2023-002",
            "invoice_date": "2023-08-15",
            "due_date": "2023-09-15",
            "partner_id": "client-002",
            "status": "posted",
            "lines": [
                {
                    "line_number": 1,
                    "unit_price": 1250.0,
                    "quantity": 2,
                    "untaxed_amount": 2500.0,
                    "tax_rate": 21.0,
                    "tax_amount": 525.0,
                    "total": 3025.0,
                    "account_number": "700000",
                    "tax_code": "tax-001",
                    "description": "Software license",
                }
            ],
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

JOURNAL_ALL = {
    "items": [
        {
            "id": "journal-001",
            "code": "SAL",
            "name": "Sales Journal",
            "journal_type": "customer_invoice",
        },
        {
            "id": "journal-003",
            "code": "BANK",
            "name": "Bank Journal",
            "journal_type": "financial_operation",
            "counterpart_account": "550000",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

ENTRY_CREATE = {
    "id": "entry-001",
    "journal_id": "journal-001",
    "date": "2023-08-01",
    "journal_name": "Sales Journal",
    "posted": True,
    "items": [
        {
            "id": "entry-line-001",
            "account_number": "101000",
            "account_name": "Cash Account",
            "description": "test debit",
            "debit": 1,
            "credit": 0,
            "currency": "EUR",
        },
        {
            "id": "entry-line-002",
            "account_number": "101000",
            "account_name": "Cash Account",
            "description": "test credit",
            "debit": 0,
            "credit": 1,
            "currency": "EUR",
        },
    ],
}

FINANCIAL_ENTRY_CREATE = {
    "id": "financial-entry-001",
    "date": "2023-08-01",
    "journal_id": "journal-003",
    "currency": "EUR",
    "number": "FE-2023-001",
    "items": [
        {
            "account_type": "general_account",
            "account": "101000",
            "amount": 1,
            "counterpart_account": "550000",
        }
    ],
}

OUTSTANDING_ALL = {
    "items": [
        {
            "id": "outstanding-001",
            "number": "INV-2023-001",
            "journal_id": "journal-001",
            "journal_type": "customer_invoice",
            "date": "2023-08-01",
            "due_date": "2023-09-01",
            "currency": "EUR",
            "currency_exchange_rate": 1.0,
            "amount": 1210.0,
            "open_amount": 1210.0,
            "partner_id": "client-001",
            "account_number": "400001",
            "posted": True,
        },
        {
            "id": "outstanding-002",
            "number": "INV-2023-002",
            "journal_id": "journal-001",
            "journal_type": "customer_invoice",
            "date": "2023-08-15",
            "due_date": "2023-09-15",
            "currency": "USD",
            "currency_exchange_rate": 0.85,
            "amount": 3025.0,
            "open_amount": 3025.0,
            "partner_id": "client-002",
            "account_number": "400002",
            "posted": True,
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

ANALYTIC_ACCOUNT_MULTI_PLAN_ALL = {
    "items": [
        {
            "id": "af26326f-af3d-4059-9a5d-00e536f3d610",
            "active": True,
            "code": None,
            "name": "rsfsd",
            "currency": "EUR",
            "balance": 0.0,
            "credit": 0.0,
            "debit": 0.0,
            "analytic_plan": "42ffc773-b77b-4719-90b6-71e8d017043d",
        },
        {
            "id": "6d01c5c3-dad4-4baf-9a5e-6635024bffba",
            "active": True,
            "code": None,
            "name": "Chantier 2",
            "currency": "EUR",
            "balance": 0.0,
            "credit": 0.0,
            "debit": 0.0,
            "analytic_plan": "0ed690d3-4686-4bd0-9474-54ec606e66a1",
        },
    ],
    "total": 28,
    "page": 1,
    "size": 2,
}

ANALYTIC_ACCOUNT_MULTI_PLAN_CREATE = {
    "id": "0198c64c-380a-7c2a-8912-79f58bf3fc94",
    "active": True,
    "code": None,
    "name": "New Project Analysis",
    "currency": "EUR",
    "balance": 0.0,
    "credit": 0.0,
    "debit": 0.0,
    "analytic_plan": "42ffc773-b77b-4719-90b6-71e8d017043d",
}

ANALYTIC_ACCOUNT_MULTI_PLAN_UPDATE = {
    "id": "af26326f-af3d-4059-9a5d-00e536f3d610",
    "active": True,
    "code": None,
    "name": "Updated Marketing Campaign",
    "currency": "EUR",
    "balance": 0.0,
    "credit": 0.0,
    "debit": 0.0,
    "analytic_plan": "42ffc773-b77b-4719-90b6-71e8d017043d",
}

FOLDERS = [
    [
        {
            "id": "folder-001",
            "name": "Folder 1",
            "selected": True,
            "vat": "21",
            "company_number": "1234567890",
            "main_currency": "EUR",
            "addresses": [
                {
                    "street": "Main Street",
                    "number": "123",
                    "box": "123",
                    "postal_code": "1000",
                    "city": "Brussels",
                    "country": "BE",
                }
            ],
        },
        {
            "id": "folder-001",
            "name": "Folder 1",
            "selected": True,
            "vat": "21",
            "company_number": "1234567890",
            "main_currency": "EUR",
            "addresses": [
                {
                    "street": "Main Street",
                    "number": "123",
                    "box": "123",
                    "postal_code": "1000",
                    "city": "Brussels",
                    "country": "BE",
                }
            ],
        },
    ]
]
