from typing import ClassVar

from chift.api.mixins import PaginationMixin, ReadMixin
from chift.openapi.models import PMSAccountingCategory as AccountingCategoryModel
from chift.openapi.models import PMSClosure as ClosureModel
from chift.openapi.models import PMSCustomer as CustomerModel
from chift.openapi.models import PMSInvoiceFull as InvoiceModel
from chift.openapi.models import PMSLocation as LocationModel
from chift.openapi.models import PMSOrder as OrderModel
from chift.openapi.models import PMSPayment as PaymentModel
from chift.openapi.models import PMSPaymentMethods as PaymentMethodsModel
from chift.openapi.models import PMSTax as TaxModel


class PmsRouter:
    def __init__(self, consumer_id, connection_id):
        self.PaymentMethod = PaymentMethod(consumer_id, connection_id)
        self.Payment = Payment(consumer_id, connection_id)
        self.Location = Location(consumer_id, connection_id)
        self.Order = Order(consumer_id, connection_id)
        self.Closure = Closure(consumer_id, connection_id)
        self.AccountingCategory = AccountingCategory(consumer_id, connection_id)
        self.Invoice = Invoice(consumer_id, connection_id)
        self.Customer = Customer(consumer_id, connection_id)
        self.Tax = Tax(consumer_id, connection_id)


class PaymentMethod(PaginationMixin[PaymentMethodsModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "payment-methods"
    model = PaymentMethodsModel


class Payment(PaginationMixin[PaymentModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "payments"
    model = PaymentModel


class Location(PaginationMixin[LocationModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "locations"
    model = LocationModel


class Closure(ReadMixin[ClosureModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "closures"
    model = ClosureModel


class Order(PaginationMixin[OrderModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "orders"
    model = OrderModel


class Invoice(PaginationMixin[InvoiceModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "invoices"
    model = InvoiceModel


class AccountingCategory(PaginationMixin[AccountingCategoryModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "accounting-categories"
    model = AccountingCategoryModel


class Customer(ReadMixin[CustomerModel], PaginationMixin[CustomerModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "customers"
    model = CustomerModel


class Tax(PaginationMixin[TaxModel]):
    chift_vertical: ClassVar = "pms"
    chift_model: ClassVar = "taxes"
    model = TaxModel
