import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra

from .openapi import (
    AccountItem,
    AnalyticAccountItemOut,
    AppRoutersAccountingVatCode,
    AppRoutersCommerceProductItem,
    BalanceItemOut,
    ClientItemOut,
    ClosureItem,
    CommerceCustomerItem,
    CommerceLocationItemOut,
    ConnectionItem,
    ConsumerItem,
    ContactItemOut,
    DataItem,
    DataItemOut,
    DataStoreItem,
    FinancialEntryItemOut,
    IntegrationItem,
    InvoiceItemOutMonoAnalyticPlan,
    InvoiceItemOutSingle,
    Journal,
    JournalEntryMultiAnalyticPlan,
    MiscellaneousOperationOut,
    ModelsInvoicingVatCode,
    OpportunityItem,
    OrderItem,
    OrderItemOut,
    OutstandingItem,
    PaymentItem,
    PaymentMethods,
    POSCustomerItem,
    POSLocationItem,
    ProductItemOut,
    ReadFlowItem,
    SalesItem,
    SupplierItemOut,
    SyncConsumerItem,
    SyncItem,
    TransactionItemOut,
    VariantItem,
    WebhookInstanceGetItem,
    WebhookItem,
)

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
    data: Optional[FlowTriggerTimer]


class FlowConfig(BaseModel):
    definitionFields: Optional[List[dict]]
    doorkeyFields: Optional[List[dict]]
    customFields: Optional[List[dict]]
    datastores: Optional[List[Datastore]] = []


# consumers


class Consumer(ConsumerItem, extra=Extra.allow):
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


class Sync(SyncItem):
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
class Connection(ConnectionItem):
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


class Tax(ModelsInvoicingVatCode):
    pass


# accouting
class AnalyticPlan(AnalyticAccountItemOut):
    pass


class TaxAccounting(AppRoutersAccountingVatCode):
    pass


class MiscellaneousOperation(MiscellaneousOperationOut):
    pass


class Account(AccountItem):
    pass


class Supplier(SupplierItemOut):
    pass


class Client(ClientItemOut):
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


class Payment(PaymentItem):
    pass


class Location(POSLocationItem):
    pass


class Order(OrderItem):
    pass


class Closure(ClosureItem):
    pass


# e-commerce
class CommerceCustomer(CommerceCustomerItem):
    pass


class CommerceProduct(AppRoutersCommerceProductItem):
    pass


class CommerceLocation(CommerceLocationItemOut):
    pass


class CommerceOrder(OrderItemOut):
    pass


class CommerceVariant(VariantItem):
    pass


# payment


class PaymentTransaction(TransactionItemOut):
    pass


class PaymentBalance(BalanceItemOut):
    pass
