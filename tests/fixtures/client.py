from uuid import uuid4

CONSUMER_ALL = [
    {
        "consumerid": str(uuid4()),
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "internal_reference": "ref-001",
        "redirect_url": "https://example.com/redirect",
    },
    {
        "consumerid": str(uuid4()),
        "name": "Bob Smith",
        "email": None,
        "internal_reference": None,
        "redirect_url": None,
    },
]
