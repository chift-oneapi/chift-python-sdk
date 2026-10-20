LEGAL_ENTITIES_ALL = [{"id": "le_1", "name": "Chift SRL"}]

LEDGER_ACCOUNTS_ALL = {
    "items": [
        {"number": "601000", "name": "Office supplies", "type": "expense"},
        {"number": "625100", "name": "Travel"},
    ],
    "total": 2,
    "page": 1,
    "size": 50,
}

PAYABLES_ALL = {
    "items": [
        {
            "id": "inv_paper",
            "payable_type": "supplier_invoice",
            "invoice_number": "OD-2026-114",
            "supplier_id": "sup_office",
            "currency": "EUR",
            "untaxed_amount": 100.0,
            "tax_amount": 21.0,
            "total": 121.0,
            "payable_date": "2026-09-02",
            "due_date": "2026-10-02",
            "export_status": "to_export",
            "lines": [
                {
                    "description": "Printer paper",
                    "quantity": 10,
                    "unit_price": 10.0,
                    "untaxed_amount": 100.0,
                    "tax_rate": 21.0,
                    "tax_amount": 21.0,
                    "total": 121.0,
                    "account_number": "601000",
                    "tax_id": "vat_21",
                }
            ],
        }
    ],
    "total": 1,
    "page": 1,
    "size": 50,
}

FINANCIAL_MOVEMENTS_ALL = {
    "items": [
        {
            "id": "mvt_1",
            "date": "2026-09-10",
            "amount": 121.0,
            "currency": "EUR",
            "type": "supplier_payment",
            "export_status": "to_export",
            "allocations": [
                {"amount": 121.0, "currency": "EUR", "payable_id": "inv_paper"}
            ],
        }
    ],
    "total": 1,
    "page": 1,
    "size": 50,
}

SUPPLIERS_ALL = {
    "items": [
        {
            "id": "sup_office",
            "name": "Office Depot",
            "external_reference": "OFFICE01",
            "vat": "BE0403200393",
        }
    ],
    "total": 1,
    "page": 1,
    "size": 50,
}
