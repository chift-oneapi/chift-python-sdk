import datetime
from uuid import uuid4

# Mock data for contacts
CONTACT_ALL = {
    "items": [
        {
            "id": "contact-001",
            "source_ref": {"id": "c-001", "model": "contact"},
            "is_prospect": False,
            "is_customer": True,
            "is_supplier": False,
            "is_company": False,
            "company_name": None,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+10000000001",
            "mobile": None,
            "company_id": None,
            "vat": None,
            "company_number": None,
            "currency": "EUR",
            "language": "en",
            "comment": None,
            "customer_account_number": "411000",
            "supplier_account_number": None,
            "addresses": [
                {
                    "address_type": "main",
                    "name": None,
                    "number": "123",
                    "box": None,
                    "phone": None,
                    "mobile": None,
                    "email": None,
                    "street": "Main Street",
                    "city": "New York",
                    "postal_code": "10001",
                    "country": "US",
                }
            ],
            "external_reference": None,
        },
        {
            "id": "contact-002",
            "source_ref": {"id": "c-002", "model": "contact"},
            "is_prospect": False,
            "is_customer": True,
            "is_supplier": False,
            "is_company": True,
            "company_name": "Acme Corp",
            "first_name": None,
            "last_name": None,
            "email": "info@acmecorp.com",
            "phone": "+10000000002",
            "mobile": None,
            "company_id": None,
            "vat": "BE0123456789",
            "company_number": "0123456789",
            "currency": "EUR",
            "language": "en",
            "comment": None,
            "customer_account_number": "411000",
            "supplier_account_number": None,
            "addresses": [
                {
                    "address_type": "main",
                    "name": None,
                    "number": "456",
                    "box": None,
                    "phone": None,
                    "mobile": None,
                    "email": None,
                    "street": "Business Avenue",
                    "city": "Brussels",
                    "postal_code": "1000",
                    "country": "BE",
                }
            ],
            "external_reference": None,
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

CONTACT_CREATE = {
    "id": "contact-test-123",
    "source_ref": {"id": "c-test-123", "model": "contact"},
    "is_prospect": False,
    "is_customer": True,
    "is_supplier": False,
    "is_company": False,
    "company_name": None,
    "first_name": "Test",
    "last_name": "Contact",
    "email": None,
    "phone": None,
    "mobile": None,
    "company_id": None,
    "vat": None,
    "company_number": None,
    "currency": "EUR",
    "language": None,
    "comment": None,
    "customer_account_number": "411000",
    "supplier_account_number": None,
    "addresses": [
        {
            "address_type": "main",
            "name": None,
            "number": None,
            "box": None,
            "phone": None,
            "mobile": None,
            "email": None,
            "street": "street",
            "city": "city",
            "postal_code": "postal_code",
            "country": "BE",
        }
    ],
    "external_reference": None,
}

CONTACT_GET = CONTACT_CREATE

# Mock data for invoices
INVOICE_ALL = {
    "items": [
        {
            "id": "invoice-001",
            "source_ref": {"id": "i-001", "model": "invoice"},
            "currency": "EUR",
            "invoice_type": "customer_invoice",
            "status": "posted",
            "invoice_date": "2025-01-15",
            "tax_amount": 210.0,
            "untaxed_amount": 1000.0,
            "total": 1210.0,
            "lines": [
                {
                    "description": "Professional Services",
                    "unit_price": 1000.0,
                    "quantity": 1,
                    "discount_amount": 0.0,
                    "tax_amount": 210.0,
                    "untaxed_amount": 1000.0,
                    "total": 1210.0,
                    "tax_rate": 21.0,
                    "account_number": "700000",
                    "tax_id": "tax-001",
                }
            ],
            "partner_id": "contact-001",
            "invoice_number": "INV-2025-001",
            "due_date": "2025-02-15",
            "reference": "PO-2025-001",
            "payment_communication": "INV-2025-001",
            "customer_memo": None,
            "last_updated_on": "2025-01-15T10:00:00Z",
            "outstanding_amount": 1210.0,
            "accounting_date": "2025-01-15",
            "payment_method_id": None,
            "currency_exchange_rate": 1.0,
        },
        {
            "id": "invoice-002",
            "source_ref": {"id": "i-002", "model": "invoice"},
            "currency": "EUR",
            "invoice_type": "customer_invoice",
            "status": "paid",
            "invoice_date": "2025-01-20",
            "tax_amount": 105.0,
            "untaxed_amount": 500.0,
            "total": 605.0,
            "lines": [
                {
                    "description": "Software License",
                    "unit_price": 500.0,
                    "quantity": 1,
                    "discount_amount": 0.0,
                    "tax_amount": 105.0,
                    "untaxed_amount": 500.0,
                    "total": 605.0,
                    "tax_rate": 21.0,
                    "account_number": "700000",
                    "tax_id": "tax-001",
                }
            ],
            "partner_id": "contact-002",
            "invoice_number": "INV-2025-002",
            "due_date": "2025-02-20",
            "reference": "PO-2025-002",
            "payment_communication": "INV-2025-002",
            "customer_memo": None,
            "last_updated_on": "2025-01-20T11:30:00Z",
            "outstanding_amount": 0.0,
            "accounting_date": "2025-01-20",
            "payment_method_id": "pm-001",
            "currency_exchange_rate": 1.0,
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

# Create a template for invoice create
today = datetime.date.today().strftime("%Y-%m-%d")
new_invoice_id = f"invoice-{uuid4().hex[:8]}"
new_invoice_number = f"INV-{datetime.date.today().strftime('%Y%m')}-TEST"

INVOICE_CREATE = {
    "id": new_invoice_id,
    "source_ref": {"id": f"i-{uuid4().hex[:8]}", "model": "invoice"},
    "currency": "EUR",
    "invoice_type": "customer_invoice",
    "status": "draft",
    "invoice_date": today,
    "tax_amount": 100.0,
    "untaxed_amount": 100.0,
    "total": 100.0,
    "lines": [
        {
            "description": "desc",
            "unit_price": 100.0,
            "quantity": 1,
            "discount_amount": 0.0,
            "tax_amount": 100.0,
            "untaxed_amount": 100.0,
            "total": 100.0,
            "tax_rate": 10.0,
            "account_number": "700000",
            "tax_id": None,
            "product_code": "123",
        }
    ],
    "partner_id": "contact-test-123",
    "invoice_number": new_invoice_number,
    "due_date": datetime.date.today()
    .replace(
        month=datetime.date.today().month + 1 if datetime.date.today().month < 12 else 1
    )
    .strftime("%Y-%m-%d"),
    "reference": None,
    "payment_communication": new_invoice_number,
    "customer_memo": None,
    "last_updated_on": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "outstanding_amount": 100.0,
    "accounting_date": today,
    "payment_method_id": None,
    "currency_exchange_rate": 1.0,
}

INVOICE_GET = INVOICE_CREATE

# Mock data for products
PRODUCT_ALL = {
    "items": [
        {
            "id": "product-001",
            "source_ref": {"id": "p-001", "model": "product"},
            "name": "Professional Services",
            "unit_price": 100.0,
            "tax_id": "tax-001",
            "code": "SERV-001",
            "unit": "hour",
            "category": "Services",
            "currency": "EUR",
            "description": "Professional consultancy services",
            "available_quantity": 0,
            "cost": 0,
        },
        {
            "id": "product-002",
            "source_ref": {"id": "p-002", "model": "product"},
            "name": "Software License",
            "unit_price": 500.0,
            "tax_id": "tax-001",
            "code": "LIC-001",
            "unit": "unit",
            "category": "Licenses",
            "currency": "EUR",
            "description": "Annual software license",
            "available_quantity": 100,
            "cost": 100.0,
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

PRODUCT_CREATE = {
    "id": "product-test-123",
    "source_ref": {"id": "p-test-123", "model": "product"},
    "name": str(uuid4()),
    "unit_price": 100.0,
    "tax_id": "tax-001",
    "code": str(uuid4())[:20],
    "unit": "U",
    "category": None,
    "currency": "EUR",
    "description": None,
    "available_quantity": 0,
    "cost": 0,
}

PRODUCT_GET = PRODUCT_CREATE

# Mock data for taxes
TAX_ALL = {
    "items": [
        {
            "id": "tax-001",
            "source_ref": {"id": "t-001", "model": "tax"},
            "label": "VAT 21%",
            "rate": 21.0,
            "type": "both",
            "code": "T21",
            "scope": "nat",
        },
        {
            "id": "tax-002",
            "source_ref": {"id": "t-002", "model": "tax"},
            "label": "VAT 6%",
            "rate": 6.0,
            "type": "both",
            "code": "T6",
            "scope": "nat",
        },
        {
            "id": "tax-003",
            "source_ref": {"id": "t-003", "model": "tax"},
            "label": "VAT 0%",
            "rate": 0.0,
            "type": "both",
            "code": "T0",
            "scope": "eu",
        },
    ],
    "total": 3,
    "page": 1,
    "size": 10,
}

TAX_GET = TAX_ALL["items"][0]

# Mock data for payment methods
PAYMENT_METHOD_ALL = {
    "items": [
        {
            "id": "pm-001",
            "source_ref": {"id": "pm-001", "model": "payment_method"},
            "name": "Bank Transfer",
            "active": True,
        },
        {
            "id": "pm-002",
            "source_ref": {"id": "pm-002", "model": "payment_method"},
            "name": "Credit Card",
            "active": True,
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

# Mock data for payments
PAYMENT_ALL = {
    "items": [
        {
            "id": "payment-001",
            "source_ref": {"id": "p-001", "model": "payment"},
            "status": "completed",
            "description": "Payment for invoice INV-2025-002",
            "amount": 605.0,
            "currency": "EUR",
            "payment_date": "2025-01-22T09:15:00Z",
            "partner_id": "contact-002",
            "payment_method_id": "pm-001",
            "payment_method_name": "Bank Transfer",
            "invoice_id": "invoice-002",
            "invoice_number": "INV-2025-002",
        },
        {
            "id": "payment-002",
            "source_ref": {"id": "p-002", "model": "payment"},
            "status": "pending",
            "description": "Payment for invoice INV-2025-003",
            "amount": 363.0,
            "currency": "EUR",
            "payment_date": "2025-01-25T14:30:00Z",
            "partner_id": "contact-001",
            "payment_method_id": "pm-002",
            "payment_method_name": "Credit Card",
            "invoice_id": "invoice-003",
            "invoice_number": "INV-2025-003",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

# Mock data for "custom" endpoints
CUSTOM_CASHES = {
    "items": [
        {
            "cashid": "cash-001",
            "name": "Main Cash Register",
            "active": True,
            "currency": "EUR",
        },
        {
            "cashid": "cash-002",
            "name": "Secondary Cash Register",
            "active": True,
            "currency": "EUR",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

CUSTOM_CASH_ENTRIES = {
    "items": [
        {
            "entryid": "entry-001",
            "cashid": "cash-001",
            "date": "2025-01-15",
            "amount": 500.0,
            "description": "Initial balance",
            "type": "in",
        },
        {
            "entryid": "entry-002",
            "cashid": "cash-001",
            "date": "2025-01-16",
            "amount": -100.0,
            "description": "Office supplies",
            "type": "out",
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}
