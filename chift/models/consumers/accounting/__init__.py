from typing import ClassVar

from chift.api.mixins import CreateMixin, PaginationMixin, ReadMixin, UpdateMixin
from chift.openapi.models import Account as AccountModel
from chift.openapi.models import (
    AnalyticAccountMultiPlan as AnalyticAccountMultiPlanModel,
)
from chift.openapi.models import AnalyticPlan as AnalyticPlanModel
from chift.openapi.models import Attachment as AttachmentModel
from chift.openapi.models import BankAccount as BankAccountModel
from chift.openapi.models import Client as ClientModel
from chift.openapi.models import Employee as EmployeeModel
from chift.openapi.models import FinancialEntry as FinancialEntryModel
from chift.openapi.models import InvoiceAccounting as InvoiceAccountingModel
from chift.openapi.models import Journal as JournalModel
from chift.openapi.models import JournalEntry as JournalEntryModel
from chift.openapi.models import Matching as MatchingModel
from chift.openapi.models import MiscellaneousOperation as MiscellaneousOperationModel
from chift.openapi.models import MultipleMatching as MultipleMatchingModel
from chift.openapi.models import Outstanding as OutstandingModel
from chift.openapi.models import Supplier as SupplierModel
from chift.openapi.models import TaxAccounting as TaxAccountingModel


class AccountingRouter:
    def __init__(self, consumer_id, connection_id):
        self.AnalyticPlan = AnalyticPlan(consumer_id, connection_id)
        self.AnalyticAccountMultiPlan = AnalyticAccountMultiPlan(
            consumer_id, connection_id
        )
        self.Tax = Tax(consumer_id, connection_id)
        self.Account = Account(consumer_id, connection_id)
        self.MiscellaneousOperation = MiscellaneousOperation(consumer_id, connection_id)
        self.Client = Client(consumer_id, connection_id)
        self.Supplier = Supplier(consumer_id, connection_id)
        self.Employee = Employee(consumer_id, connection_id)
        self.Invoice = Invoice(consumer_id, connection_id)
        self.JournalEntry = JournalEntry(consumer_id, connection_id)
        self.FinancialEntry = FinancialEntry(consumer_id, connection_id)
        self.Outstanding = Outstanding(consumer_id, connection_id)
        self.Journal = Journal(consumer_id, connection_id)
        self.Entry = Entry(consumer_id, connection_id)
        self.EntryMatching = EntryMatching(consumer_id, connection_id)
        self.MultipleEntryMatching = MultipleEntryMatching(consumer_id, connection_id)
        self.Attachment = Attachment(consumer_id, connection_id)
        self.BankAccount = BankAccount(consumer_id, connection_id)


class AnalyticPlan(PaginationMixin[AnalyticPlanModel]):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "analytic-plans"
    model = AnalyticPlanModel


class AnalyticAccountMultiPlan(
    CreateMixin[AnalyticAccountMultiPlanModel],
    PaginationMixin[AnalyticAccountMultiPlanModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "analytic-accounts/multi-analytic-plans"
    model = AnalyticAccountMultiPlanModel


class Tax(PaginationMixin[TaxAccountingModel]):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "vat-codes"
    model = TaxAccountingModel


class MiscellaneousOperation(
    ReadMixin[MiscellaneousOperationModel],
    PaginationMixin[MiscellaneousOperationModel],
    CreateMixin[MiscellaneousOperationModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "miscellaneous-operation"
    model = MiscellaneousOperationModel


class Account(
    ReadMixin[AccountModel],
    PaginationMixin[AccountModel],
    CreateMixin[AccountModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "chart-of-accounts"
    chift_model_create: ClassVar = "accounts"
    model = AccountModel


class Supplier(
    ReadMixin[SupplierModel],
    PaginationMixin[SupplierModel],
    CreateMixin[SupplierModel],
    UpdateMixin[SupplierModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "suppliers"
    model = SupplierModel


class Client(
    ReadMixin[ClientModel],
    PaginationMixin[ClientModel],
    CreateMixin[ClientModel],
    UpdateMixin[ClientModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "clients"
    model = ClientModel


class Invoice(
    ReadMixin[InvoiceAccountingModel],
    PaginationMixin[InvoiceAccountingModel],
    CreateMixin[InvoiceAccountingModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "invoices"
    model = InvoiceAccountingModel

    def all(self, invoice_type, params=None, client=None, limit=None):
        self.extra_path = f"type/{invoice_type}"
        return super().all(params=params, limit=limit, client=client)


# deprecated
class JournalEntry(
    PaginationMixin[JournalEntryModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "journal/entries"
    model = JournalEntryModel


class Entry(
    CreateMixin[JournalEntryModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "journal-entries"
    model = JournalEntryModel


class FinancialEntry(
    CreateMixin[FinancialEntryModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "financial-entries"
    model = FinancialEntryModel


class Outstanding(
    PaginationMixin[OutstandingModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "outstandings"
    model = OutstandingModel


class Journal(
    CreateMixin[JournalModel],
    PaginationMixin[JournalModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "journals"
    chift_model_create: ClassVar = "journal"
    model = JournalModel


class EntryMatching(CreateMixin[MatchingModel]):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "matching"
    model = MatchingModel


class MultipleEntryMatching(CreateMixin[MultipleMatchingModel]):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "matching-multiple"
    model = MultipleMatchingModel


class Employee(PaginationMixin[EmployeeModel]):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "employees"
    model = EmployeeModel


class Attachment(CreateMixin[MatchingModel], PaginationMixin[AttachmentModel]):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "attachments"
    model = AttachmentModel

    def create(self, invoice_id, data, client=None, params=None):
        self.chift_model = "invoices"
        self.extra_path = f"pdf/{invoice_id}"
        return super().create(data=data, client=client, params=params, map_model=False)


class BankAccount(CreateMixin[BankAccountModel]):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "bank-accounts"
    model = BankAccountModel
