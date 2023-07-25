import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra

from .openapi import (
    AccountItem,
    AnalyticAccountItemOut,
    BackboneBackboneApiAppRoutersAccountingVatCode,
    BackboneBackboneApiAppRoutersCommerceProductItem,
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
    IntegrationItem,
    InvoiceItemOut,
    InvoiceItemOutMonoAnalyticPlan,
    MiscellaneousOperationOut,
    ModelsInvoicingVatCode,
    OpportunityItem,
    OrderItem,
    OrderItemOut,
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
    WebhookInstanceGetItem,
    WebhookItem,
    JournalEntryMultiAnalyticPlan,
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
    def connection(self):
        from chift.models.consumers.connection import (
            ConnectionRouter,
        )  # avoid circular import

        return ConnectionRouter(self.consumerid, self.connectionid)

    @property
    def datastore(self):
        from chift.models.consumers.data import DataRouter  # avoid circular import

        return DataRouter(self.consumerid, self.connectionid)

    @property
    def sync(self):
        from chift.models.consumers.sync import SyncRouter  # avoid circular import

        return SyncRouter(self.consumerid, self.connectionid)

    @property
    def log(self):
        from chift.models.consumers.log import LogRouter  # avoid circular import

        return LogRouter(self.consumerid, self.connectionid)

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
    pass


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


class Invoice(InvoiceItemOut):
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


class TaxAccounting(BackboneBackboneApiAppRoutersAccountingVatCode):
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


class CommerceProduct(BackboneBackboneApiAppRoutersCommerceProductItem):
    pass


class CommerceLocation(CommerceLocationItemOut):
    pass


class CommerceOrder(OrderItemOut):
    pass
