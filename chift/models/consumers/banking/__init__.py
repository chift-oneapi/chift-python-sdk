from typing import ClassVar

from chift.api.mixins import ListMixin, PaginationMixin
from chift.openapi.models import BankingAccount as BankingAccountModel
from chift.openapi.models import BankingAttachment as BankingAttachmentModel
from chift.openapi.models import BankingCounterpart as BankingCounterpartModel
from chift.openapi.models import (
    BankingFinancialInstitution as FinancialInstitutionModel,
)
from chift.openapi.models import BankingTransaction as BankingTransactionModel


class BankingRouter:
    def __init__(self, consumer_id, connection_id):
        self.FinancialInstitution = FinancialInstitution(consumer_id, connection_id)
        self.Account = Account(consumer_id, connection_id)
        self.Transaction = Transaction(consumer_id, connection_id)
        self.Counterpart = Counterpart(consumer_id, connection_id)
        self.Attachment = Attachment(consumer_id, connection_id)


class FinancialInstitution(PaginationMixin[FinancialInstitutionModel]):
    chift_vertical: ClassVar = "banking"
    chift_model: ClassVar = "financial-institutions"
    model = FinancialInstitutionModel


class Account(PaginationMixin[BankingAccountModel]):
    chift_vertical: ClassVar = "banking"
    chift_model: ClassVar = "accounts"
    model = BankingAccountModel


class Transaction(PaginationMixin[BankingTransactionModel]):
    chift_vertical: ClassVar = "banking"
    chift_model: ClassVar = "transactions"
    model = BankingTransactionModel


class Counterpart(PaginationMixin[BankingCounterpartModel]):
    chift_vertical: ClassVar = "banking"
    chift_model: ClassVar = "counterparts"
    model = BankingCounterpartModel


class Attachment(ListMixin[BankingAttachmentModel]):
    chift_vertical: ClassVar = "banking"
    chift_model: ClassVar = "attachments"
    model = BankingAttachmentModel
