from typing import ClassVar

from chift.api.mixins import CreateMixin, PaginationMixin, ReadMixin, UpdateMixin
from chift.openapi.models import PaymentBalance as PaymentBalanceModel
from chift.openapi.models import PaymentTransaction as TransactionModel


class PaymentRouter:
    def __init__(self, consumer_id, connection_id):
        self.Transaction = Transaction(consumer_id, connection_id)
        self.Balance = Balance(consumer_id, connection_id)


class Transaction(PaginationMixin[TransactionModel]):
    chift_vertical: ClassVar = "payment"
    chift_model: ClassVar = "transactions"
    model = TransactionModel


class Balance(PaginationMixin[PaymentBalanceModel]):
    chift_vertical: ClassVar = "payment"
    chift_model: ClassVar = "balances"
    model = PaymentBalanceModel
