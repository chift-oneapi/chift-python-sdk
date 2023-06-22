from __future__ import annotations

from typing import ClassVar

from chift.api.mixins import CreateMixin, PaginationMixin, ReadMixin
from chift.openapi.models import Contact as ContactModel
from chift.openapi.models import Invoice as InvoiceModel
from chift.openapi.models import Opportunity as OpportunityModel
from chift.openapi.models import Product as ProductModel
from chift.openapi.models import Tax as TaxModel


class InvoicingRouter:
    def __init__(self, consumer_id, connection_id):
        self.Product = Product(consumer_id, connection_id)
        self.Invoice = Invoice(consumer_id, connection_id)
        self.Contact = Contact(consumer_id, connection_id)
        self.Opportunity = Opportunity(consumer_id, connection_id)
        self.Tax = Tax(consumer_id, connection_id)


class Product(
    ReadMixin[ProductModel],
    PaginationMixin[ProductModel],
    CreateMixin[ProductModel],
):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "products"
    model = ProductModel


class Invoice(
    ReadMixin[InvoiceModel],
    CreateMixin[InvoiceModel],
    PaginationMixin[InvoiceModel],
):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "invoices"
    model = InvoiceModel


class Contact(
    ReadMixin[ContactModel],
    CreateMixin[ContactModel],
    PaginationMixin[ContactModel],
):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "contacts"
    model = ContactModel


class Opportunity(
    ReadMixin[OpportunityModel],
    CreateMixin[OpportunityModel],
    PaginationMixin[OpportunityModel],
):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "opportunities"
    model = OpportunityModel


class Tax(ReadMixin[TaxModel], PaginationMixin[TaxModel]):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "taxes"
    model = TaxModel
