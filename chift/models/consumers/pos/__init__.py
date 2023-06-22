from typing import ClassVar

from chift.api.mixins import CreateMixin, PaginationMixin, ReadMixin
from chift.openapi.models import Closure as ClosureModel
from chift.openapi.models import Customer as CustomerModel
from chift.openapi.models import Location as LocationModel
from chift.openapi.models import Order as OrderModel
from chift.openapi.models import Payment as PaymentModel
from chift.openapi.models import PaymentMethods as PaymentMethodsModel
from chift.openapi.models import Sales as SalesModel


class PosRouter:
    def __init__(self, consumer_id, connection_id):
        self.Customer = Customer(consumer_id, connection_id)
        self.PaymentMethod = PaymentMethod(consumer_id, connection_id)
        self.Sale = Sale(consumer_id, connection_id)
        self.Payment = Payment(consumer_id, connection_id)
        self.Location = Location(consumer_id, connection_id)
        self.Order = Order(consumer_id, connection_id)
        self.Closure = Closure(consumer_id, connection_id)


class Customer(
    ReadMixin[CustomerModel], PaginationMixin[CustomerModel], CreateMixin[CustomerModel]
):
    chift_vertical: ClassVar = "pos"
    chift_model: ClassVar = "customers"
    model = CustomerModel


class PaymentMethod(PaginationMixin[PaymentMethodsModel]):
    chift_vertical: ClassVar = "pos"
    chift_model: ClassVar = "payment-methods"
    model = PaymentMethodsModel


class Sale(PaginationMixin[SalesModel]):
    chift_vertical: ClassVar = "pos"
    chift_model: ClassVar = "sales"
    model = SalesModel


class Payment(PaginationMixin[PaymentModel]):
    chift_vertical: ClassVar = "pos"
    chift_model: ClassVar = "payments"
    model = PaymentModel


class Location(PaginationMixin[LocationModel]):
    chift_vertical: ClassVar = "pos"
    chift_model: ClassVar = "locations"
    model = LocationModel


class Closure(ReadMixin[ClosureModel]):
    chift_vertical: ClassVar = "pos"
    chift_model: ClassVar = "closures"
    model = ClosureModel


class Order(ReadMixin[OrderModel], PaginationMixin[OrderModel]):
    chift_vertical: ClassVar = "pos"
    chift_model: ClassVar = "orders"
    model = OrderModel
