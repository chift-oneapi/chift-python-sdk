import uuid
from datetime import datetime

# Response for Transaction.all()
TRANSACTIONS_ALL = {
    "items": [
        {
            "id": str(uuid.uuid4()),
            "source_ref": {"id": "tx_123", "model": "Transaction"},
            "total": 100.0,
            "fee": 2.5,
            "amount": 100,
            "currency": "EUR",
            "exchange_rate": 1.0,
            "create_date": datetime.now().isoformat(),
            "application_type": "payment",
            "accounting_category": "payment",
            "refund_id": None,
            "payment_id": str(uuid.uuid4()),
        },
        {
            "id": str(uuid.uuid4()),
            "source_ref": {"id": "tx_124", "model": "Transaction"},
            "total": 75.0,
            "fee": 1.5,
            "amount": 100,
            "currency": "EUR",
            "exchange_rate": 1.0,
            "create_date": datetime.now().isoformat(),
            "application_type": "payout",
            "accounting_category": "payout",
            "refund_id": None,
            "payment_id": None,
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

# Response for Balance.all()
BALANCES_ALL = {
    "items": [
        {
            "id": str(uuid.uuid4()),
            "source_ref": {"id": "bal_123", "model": "Balance"},
            "available_amount": 1500.0,
            "currency": "EUR",
            "create_date": datetime.now().isoformat(),
        },
        {
            "id": str(uuid.uuid4()),
            "source_ref": {"id": "bal_124", "model": "Balance"},
            "available_amount": 500.0,
            "currency": "USD",
            "create_date": datetime.now().isoformat(),
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

# Generate payment ID for consistent references
PAYMENT_ID = str(uuid.uuid4())

# Response for Payment.all()
PAYMENTS_ALL = {
    "items": [
        {
            "id": PAYMENT_ID,
            "source_ref": {"id": "pay_123", "model": "Payment"},
            "status": "completed",
            "description": "Test payment",
            "amount": 100.0,
            "currency": "EUR",
            "payment_date": datetime.now().isoformat(),
            "partner_id": str(uuid.uuid4()),
            "payment_id": "pay_124",
        },
        {
            "id": str(uuid.uuid4()),
            "source_ref": {"id": "pay_124", "model": "Payment"},
            "status": "completed",
            "description": "Another payment",
            "amount": 75.0,
            "currency": "EUR",
            "payment_date": datetime.now().isoformat(),
            "payment_id": "pay_123",
            "partner_id": str(uuid.uuid4()),
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}

# Response for Payment.get()
PAYMENT_GET = {
    "id": PAYMENT_ID,
    "source_ref": {"id": "pay_123", "model": "Payment"},
    "status": "completed",
    "description": "Test payment",
    "amount": 100.0,
    "currency": "EUR",
    "payment_date": datetime.now().isoformat(),
    "partner_id": str(uuid.uuid4()),
}

# Response for Refund.all()
REFUNDS_ALL = {
    "items": [
        {
            "id": str(uuid.uuid4()),
            "source_ref": {"id": "ref_123", "model": "Refund"},
            "status": "completed",
            "description": "Test refund",
            "amount": 25.0,
            "currency": "EUR",
            "refund_date": datetime.now().isoformat(),
            "payment_id": PAYMENT_ID,
        },
        {
            "id": str(uuid.uuid4()),
            "source_ref": {"id": "ref_124", "model": "Refund"},
            "status": "completed",
            "description": "Another refund",
            "amount": 15.0,
            "currency": "EUR",
            "refund_date": datetime.now().isoformat(),
            "payment_id": PAYMENT_ID,
        },
    ],
    "total": 2,
    "page": 1,
    "size": 10,
}
