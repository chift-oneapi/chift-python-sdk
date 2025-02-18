from __future__ import annotations

from typing import ClassVar

from chift.api.mixins import CreateMixin, PaginationMixin, ReadMixin, UpdateMixin
from chift.openapi.models import Contact as ContactModel
from chift.openapi.models import Invoice as InvoiceModel
from chift.openapi.models import InvoicingPayment as PaymentModel
from chift.openapi.models import InvoicingPaymentMethod as PaymentMethodModel
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
        self.Payment = Payment(consumer_id, connection_id)
        self.PaymentMethod = PaymentMethod(consumer_id, connection_id)
        self.UploadDocument = UploadDocument(consumer_id, connection_id)
        self.Custom = Custom(consumer_id, connection_id)


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


class Payment(
    PaginationMixin[PaymentModel],
):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "payments"
    model = PaymentModel


class PaymentMethod(
    PaginationMixin[PaymentMethodModel],
):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "payment-methods"
    model = PaymentMethodModel


class UploadDocument(CreateMixin):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "upload-document"
    model = InvoiceModel


class Custom(ReadMixin, CreateMixin, UpdateMixin, PaginationMixin):
    chift_vertical: ClassVar = "invoicing"
    chift_model: ClassVar = "custom"

    def all(self, custom_path, params=None, client=None, limit=None):
        self.extra_path = custom_path
        return super().all(params=params, map_model=False, client=client, limit=limit)

    def create(self, custom_path, data, client=None, params=None):
        self.extra_path = custom_path
        return super().create(data, map_model=False, client=client, params=params)

    def update(self, custom_path, chift_id, data, client=None, params=None):
        self.extra_path = f"{custom_path}/{chift_id}"
        return super().update(None, data, map_model=False, client=client, params=params)

    def get(self, custom_path, chift_id, params=None, client=None):
        self.extra_path = f"{custom_path}/{chift_id}"
        return super().get(chift_id=None, map_model=False, params=params, client=client)
