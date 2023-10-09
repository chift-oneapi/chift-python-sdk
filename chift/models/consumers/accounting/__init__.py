from typing import ClassVar

from chift.api.mixins import CreateMixin, PaginationMixin, ReadMixin, UpdateMixin
from chift.openapi.models import Account as AccountModel
from chift.openapi.models import AnalyticPlan as AnalyticPlanModel
from chift.openapi.models import Client as ClientModel
from chift.openapi.models import FinancialEntry as FinancialEntryModel
from chift.openapi.models import InvoiceAccounting as InvoiceAccountingModel
from chift.openapi.models import Journal as JournalModel
from chift.openapi.models import JournalEntry as JournalEntryModel
from chift.openapi.models import MiscellaneousOperation as MiscellaneousOperationModel
from chift.openapi.models import Outstanding as OutstandingModel
from chift.openapi.models import Supplier as SupplierModel
from chift.openapi.models import TaxAccounting as TaxAccountingModel


class AccountingRouter:
    def __init__(self, consumer_id, connection_id):
        self.AnalyticPlan = AnalyticPlan(consumer_id, connection_id)
        self.Tax = Tax(consumer_id, connection_id)
        self.Account = Account(consumer_id, connection_id)
        self.MiscellaneousOperation = MiscellaneousOperation(consumer_id, connection_id)
        self.Client = Client(consumer_id, connection_id)
        self.Supplier = Supplier(consumer_id, connection_id)
        self.Invoice = Invoice(consumer_id, connection_id)
        self.JournalEntry = JournalEntry(consumer_id, connection_id)
        self.FinancialEntry = FinancialEntry(consumer_id, connection_id)
        self.Outstanding = Outstanding(consumer_id, connection_id)
        self.Journal = Journal(consumer_id, connection_id)
        self.Entry = Entry(consumer_id, connection_id)


class AnalyticPlan(PaginationMixin[AnalyticPlanModel]):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "analytic-plans"
    model = AnalyticPlanModel


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

    def all(self, invoice_type, limit=None, client=None):
        self.extra_path = f"type/{invoice_type}"
        return super().all(limit=limit, client=client)


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
    chift_model: ClassVar = "financial-entry"
    model = FinancialEntryModel


class Outstanding(
    PaginationMixin[OutstandingModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "outstandings"
    model = OutstandingModel


class Journal(
    PaginationMixin[JournalModel],
):
    chift_vertical: ClassVar = "accounting"
    chift_model: ClassVar = "journals"
    model = JournalModel
