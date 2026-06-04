from typing import ClassVar

from chift.api.mixins import CreateMixin, ListMixin, PaginationMixin, ReadMixin
from chift.openapi.models import BankingAccount as BankingAccountModel
from chift.openapi.models import BankingAttachment as BankingAttachmentModel
from chift.openapi.models import BankingCounterpart as BankingCounterpartModel
from chift.openapi.models import (
    BankingFinancialInstitution as FinancialInstitutionModel,
)
from chift.openapi.models import BankingOpenBalance as BankingOpenBalanceModel
from chift.openapi.models import BankingTransaction as BankingTransactionModel


class BankingRouter:
    def __init__(self, consumer_id, connection_id):
        self.FinancialInstitution = FinancialInstitution(consumer_id, connection_id)
        self.Account = Account(consumer_id, connection_id)
        self.Transaction = Transaction(consumer_id, connection_id)
        self.Counterpart = Counterpart(consumer_id, connection_id)
        self.Attachment = Attachment(consumer_id, connection_id)
        self.OpenBalance = OpenBalance(consumer_id, connection_id)
        self.Custom = Custom(consumer_id, connection_id)


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


class OpenBalance(ReadMixin[BankingOpenBalanceModel]):
    chift_vertical: ClassVar = "banking"
    chift_model: ClassVar = "open-balance"
    model = BankingOpenBalanceModel

    def get(self, client=None, params=None):
        """Fetch the opening balance for an account on a specific date.

        ``params`` should include ``account_id`` and ``date``.
        """
        return super().get(chift_id=None, client=client, params=params)


class Custom(CreateMixin):
    chift_vertical: ClassVar = "banking"

    def __init__(self, consumer_id, connection_id, model="custom"):
        super().__init__(consumer_id, connection_id)
        self.chift_model = model

    def create(self, custom_path, data, client=None, params=None):
        self.chift_model = custom_path
        self.chift_model_create = custom_path
        return super().create(data, map_model=False, client=client, params=params)
