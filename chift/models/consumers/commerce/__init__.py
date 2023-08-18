from typing import ClassVar

from chift.api.mixins import PaginationMixin, ReadMixin
from chift.openapi.models import CommerceCustomer as CommerceCustomerModel
from chift.openapi.models import CommerceLocation as CommerceLocationModel
from chift.openapi.models import CommerceOrder as CommerceOrderModel
from chift.openapi.models import CommerceProduct as CommerceProductModel
from chift.openapi.models import CommerceVariant as CommerceVariantModel


class CommerceRouter:
    def __init__(self, consumer_id, connection_id):
        self.Customer = Customer(consumer_id, connection_id)
        self.Product = Product(consumer_id, connection_id)
        self.Location = Location(consumer_id, connection_id)
        self.Order = Order(consumer_id, connection_id)
        self.Variant = Variant(consumer_id, connection_id)


class Customer(
    ReadMixin[CommerceCustomerModel],
    PaginationMixin[CommerceCustomerModel],
):
    chift_vertical: ClassVar = "commerce"
    chift_model: ClassVar = "customers"
    model = CommerceCustomerModel


class Product(
    ReadMixin[CommerceProductModel],
    PaginationMixin[CommerceProductModel],
):
    chift_vertical: ClassVar = "commerce"
    chift_model: ClassVar = "products"
    model = CommerceProductModel


class Variant(
    ReadMixin[CommerceVariantModel],
    PaginationMixin[CommerceVariantModel],
):
    chift_vertical: ClassVar = "commerce"
    chift_model: ClassVar = "variants"
    model = CommerceVariantModel


class Location(
    PaginationMixin[CommerceLocationModel],
):
    chift_vertical: ClassVar = "commerce"
    chift_model: ClassVar = "locations"
    model = CommerceLocationModel


class Order(
    ReadMixin[CommerceOrderModel],
    PaginationMixin[CommerceOrderModel],
):
    chift_vertical: ClassVar = "commerce"
    chift_model: ClassVar = "orders"
    model = CommerceOrderModel
