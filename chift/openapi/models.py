import datetime
from enum import Enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

from .openapi import (
    AccountingCategoryItem,
    AccountingVatCode,
    AccountItem,
    AnalyticAccountItemOutMultiAnalyticPlans,
    AnalyticPlanItem,
    AttachmentItemOut,
    BackboneApiAppRoutersConnectionsConnectionItem,
    BackboneCommonModelsPosCommonProductCategoryItem,
    BalanceItemOut,
    BankAccountItemOut,
    CategoryItem,
    ClientItemOut,
    ClosureItem,
    CommerceCustomerItem,
    CommerceLocationItemOut,
    ConsumerItem,
    ContactItemOut,
    CountryItem,
    DataItem,
    DataItemOut,
    DataStoreItem,
    EmployeeItem,
    FinancialEntryItemOut,
    IntegrationItem,
    InvoiceItemOutMonoAnalyticPlan,
    InvoiceItemOutSingle,
    InvoicingPaymentItem,
    InvoicingPaymentMethodItem,
    InvoicingVatCode,
    Journal,
    JournalEntryMultiAnalyticPlan,
    LinkItem,
    MatchingOut,
    MiscellaneousOperationOut,
    MultipleMatchingOut,
    OpportunityItem,
    OrderItemOut,
    OutstandingItem,
    PaymentItemOut,
    PaymentMethodItem,
    PaymentMethods,
    PMSAccountingCategoryItem,
    PMSClosureItem,
    PMSCustomerItem,
    PMSInvoiceFullItem,
    PMSLocationItem,
    PMSOrderItem,
    PMSPaymentItem,
    PMSPaymentMethods,
    PMSTaxRateItem,
    POSCustomerItem,
    POSLocationItem,
    POSOrderItem,
    POSPaymentItem,
    POSProductItem,
    ProductItemOut,
    ProductItemOutput,
    ReadFlowItem,
    ReadSyncItem,
    RefundItemOut,
    SalesItem,
    SupplierItemOut,
    SyncConsumerItem,
    TaxRateItem,
    TransactionItemOut,
    VariantItem,
    WebhookInstanceGetItem,
    WebhookItem,
)

VarModel = TypeVar("VarModel", bound=BaseModel)

# UNPUBLISHED MODELS


class DatastoreColumn(BaseModel):
    name: str
    title: str
    type: str


class DatastoreDef(BaseModel):
    columns: List[DatastoreColumn]


class Datastore(BaseModel):
    id: Optional[str] = None
    name: str
    definition: DatastoreDef


class LogType(str, Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"


class ConsumerLog(BaseModel):
    logid: str
    type: LogType
    message: str
    when: datetime.datetime
    context: Optional[dict] = None

    model_config = ConfigDict(coerce_numbers_to_str=True)


class ExecutionType(str, Enum):
    CODE = "code"
    CHAIN = "chain"


class TriggerType(str, Enum):
    TIMER = "timer"
    EVENT = "event"


class FlowExecutionCode(BaseModel):
    code: str


class FlowExecutionChain(BaseModel):
    id: str


class FlowTriggerTimer(BaseModel):
    cronschedule: str = "*/5 * * * *"


class FlowTrigger(BaseModel):
    type: TriggerType
    data: Optional[FlowTriggerTimer] = None


class FlowConfig(BaseModel):
    definitionFields: Optional[List[dict]] = None
    doorkeyFields: Optional[List[dict]] = None
    customFields: Optional[List[dict]] = None
    datastores: Optional[List[Datastore]] = []


# consumers


class Consumer(ConsumerItem, extra="allow"):
    connectionid: str = None

    @property
    def invoicing(self):
        from chift.models.consumers.invoicing import (
            InvoicingRouter,
        )  # avoid circular import

        return InvoicingRouter(self.consumerid, self.connectionid)

    @property
    def accounting(self):
        from chift.models.consumers.accounting import (
            AccountingRouter,
        )  # avoid circular import

        return AccountingRouter(self.consumerid, self.connectionid)

    @property
    def pos(self):
        from chift.models.consumers.pos import PosRouter  # avoid circular import

        return PosRouter(self.consumerid, self.connectionid)

    @property
    def pms(self):
        from chift.models.consumers.pms import PmsRouter  # avoid circular import

        return PmsRouter(self.consumerid, self.connectionid)

    @property
    def commerce(self):
        from chift.models.consumers.commerce import (
            CommerceRouter,
        )  # avoid circular import

        return CommerceRouter(self.consumerid, self.connectionid)

    @property
    def payment(self):
        from chift.models.consumers.payment import (
            PaymentRouter,
        )  # avoid circular import

        return PaymentRouter(self.consumerid, self.connectionid)

    @property
    def custom(self):
        from chift.models.consumers.custom import CustomRouter  # avoid circular import

        return CustomRouter(self.consumerid, self.connectionid)

    @property
    def Connection(self):
        from chift.models.consumers.connection import (
            Connection,
        )  # avoid circular import

        return Connection(self.consumerid, self.connectionid)

    @property
    def Data(self):
        from chift.models.consumers.data import Data  # avoid circular import

        return Data(self.consumerid, self.connectionid)

    @property
    def Sync(self):
        from chift.models.consumers.sync import Sync  # avoid circular import

        return Sync(self.consumerid, self.connectionid)

    @property
    def Log(self):
        from chift.models.consumers.log import Log  # avoid circular import

        return Log(self.consumerid, self.connectionid)


# syncs


class Sync(ReadSyncItem):
    pass


class SyncConsumer(SyncConsumerItem):
    pass


# flow


class Flow(ReadFlowItem):
    pass


# datastores


class Datastore(DataStoreItem):
    pass


class DataIn(DataItem):
    pass


class Data(DataItemOut):
    id: Optional[str] = None


# webhook


class WebhookInstance(WebhookInstanceGetItem):
    pass


class WebhookType(WebhookItem):
    pass


# connections
class Connection(BackboneApiAppRoutersConnectionsConnectionItem):
    pass


class ConnectionLink(LinkItem):
    pass


# integrations
class Integration(IntegrationItem):
    pass


# invoicing


class Invoice(InvoiceItemOutSingle):
    pass


class Contact(ContactItemOut):
    pass


class Product(ProductItemOut):
    pass


class Opportunity(OpportunityItem):
    pass


class Tax(InvoicingVatCode):
    pass


class InvoicingPayment(InvoicingPaymentItem):
    pass


class InvoicingPaymentMethod(InvoicingPaymentMethodItem):
    pass


# accounting
class AnalyticPlan(AnalyticPlanItem):
    pass


class AnalyticAccountMultiPlan(AnalyticAccountItemOutMultiAnalyticPlans):
    pass


class TaxAccounting(AccountingVatCode):
    pass


class MiscellaneousOperation(MiscellaneousOperationOut):
    pass


class Account(AccountItem):
    pass


class Supplier(SupplierItemOut):
    pass


class Client(ClientItemOut):
    pass


class Employee(EmployeeItem):
    pass


class InvoiceAccounting(InvoiceItemOutMonoAnalyticPlan):
    pass


class JournalEntry(JournalEntryMultiAnalyticPlan):
    pass


class FinancialEntry(FinancialEntryItemOut):
    pass


class Outstanding(OutstandingItem):
    pass


class Journal(Journal):
    pass


class Matching(MatchingOut):
    pass


class MultipleMatching(MultipleMatchingOut):
    pass


class Attachment(AttachmentItemOut):
    pass


class BankAccount(BankAccountItemOut):
    pass


# log
class Log(ConsumerLog):
    pass


# pos
class Customer(POSCustomerItem):
    pass


class PaymentMethods(PaymentMethods):
    pass


class Sales(SalesItem):
    pass


class Payment(POSPaymentItem):
    pass


class Location(POSLocationItem):
    pass


class Order(POSOrderItem):
    pass


class Closure(ClosureItem):
    pass


class POSProductCategory(BackboneCommonModelsPosCommonProductCategoryItem):
    pass


class POSAccountingCategory(AccountingCategoryItem):
    pass


class POSProduct(POSProductItem):
    pass


# pms


class PMSPaymentMethods(PMSPaymentMethods):
    pass


class PMSPayment(PMSPaymentItem):
    pass


class PMSLocation(PMSLocationItem):
    pass


class PMSOrder(PMSOrderItem):
    pass


class PMSClosure(PMSClosureItem):
    pass


class PMSAccountingCategory(PMSAccountingCategoryItem):
    pass


class PMSInvoiceFull(PMSInvoiceFullItem):
    pass


class PMSCustomer(PMSCustomerItem):
    pass


class PMSTax(PMSTaxRateItem):
    pass


# e-commerce
class CommerceCustomer(CommerceCustomerItem):
    pass


class CommerceProduct(ProductItemOutput):
    pass


class CommerceLocation(CommerceLocationItemOut):
    pass


class CommerceOrder(OrderItemOut):
    pass


class CommerceVariant(VariantItem):
    pass


class CommercePaymentMethod(PaymentMethodItem):
    pass


class CommerceProductCategory(CategoryItem):
    pass


class CommerceCountry(CountryItem):
    pass


class CommerceTax(TaxRateItem):
    pass


# payment


class PaymentTransaction(TransactionItemOut):
    pass


class PaymentBalance(BalanceItemOut):
    pass


class PaymentPayment(PaymentItemOut):
    pass


class PaymentRefund(RefundItemOut):
    pass


class ObjectWithRawData(BaseModel, Generic[VarModel]):
    chift_data: VarModel
    raw_data: dict
