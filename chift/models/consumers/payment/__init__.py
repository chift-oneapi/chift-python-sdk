from typing import ClassVar

from chift.api.mixins import CreateMixin, PaginationMixin, ReadMixin, UpdateMixin
from chift.openapi.models import PaymentTransaction as TransactionModel


class PaymentRouter:
    def __init__(self, consumer_id, connection_id):
        self.Transaction = Transaction(consumer_id, connection_id)


class Transaction(PaginationMixin[TransactionModel]):
    chift_vertical: ClassVar = "payment"
    chift_model: ClassVar = "transactions"
    model = TransactionModel
