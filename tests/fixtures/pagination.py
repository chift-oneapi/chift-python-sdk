PAGINATION_MANY_DATA = [
    {
        "total": 150,
        "page": 1,
        "size": 50,
        "items": [{"id": _id} for _id in range(50)],
    },
    {
        "total": 150,
        "page": 2,
        "size": 50,
        "items": [{"id": _id} for _id in range(50, 100)],
    },
    {
        "total": 150,
        "page": 3,
        "size": 50,
        "items": [{"id": _id} for _id in range(100, 150)],
    },
]
