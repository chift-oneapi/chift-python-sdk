from typing import ClassVar

from chift.api.mixins import (
    CreateMixin,
    ListMixin,
    PaginationMixin,
    ReadMixin,
    UpdateMixin,
)
from chift.openapi.models import Account as AccountModel
from chift.openapi.models import AnalyticAccountMultiPlan as AnalyticAccountModel
from chift.openapi.models import AnalyticPlan as AnalyticPlanModel
from chift.openapi.models import Employee as EmployeeModel
from chift.openapi.models import SpendFinancialMovement as FinancialMovementModel
from chift.openapi.models import SpendLegalEntity as LegalEntityModel
from chift.openapi.models import SpendPayable as PayableModel
from chift.openapi.models import SpendSupplier as SupplierModel
from chift.openapi.models import SpendTaxCode as TaxCodeModel


class SpendManagementRouter:
    def __init__(self, consumer_id, connection_id):
        self.LegalEntity = LegalEntity(consumer_id, connection_id)
        self.LedgerAccount = LedgerAccount(consumer_id, connection_id)
        self.TaxCode = TaxCode(consumer_id, connection_id)
        self.AnalyticPlan = AnalyticPlan(consumer_id, connection_id)
        self.AnalyticAccount = AnalyticAccount(consumer_id, connection_id)
        self.Payable = Payable(consumer_id, connection_id)
        self.FinancialMovement = FinancialMovement(consumer_id, connection_id)
        self.Supplier = Supplier(consumer_id, connection_id)
        self.Employee = Employee(consumer_id, connection_id)


class LegalEntity(ListMixin[LegalEntityModel]):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "legal-entities"
    model = LegalEntityModel


class LedgerAccount(
    CreateMixin[AccountModel], PaginationMixin[AccountModel], UpdateMixin[AccountModel]
):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "ledger-accounts"
    model = AccountModel


class TaxCode(
    CreateMixin[TaxCodeModel], PaginationMixin[TaxCodeModel], UpdateMixin[TaxCodeModel]
):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "tax-codes"
    model = TaxCodeModel


class AnalyticPlan(
    CreateMixin[AnalyticPlanModel],
    PaginationMixin[AnalyticPlanModel],
    UpdateMixin[AnalyticPlanModel],
):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "analytical-plans"
    model = AnalyticPlanModel


class AnalyticAccount(
    CreateMixin[AnalyticAccountModel],
    ReadMixin[AnalyticAccountModel],
    UpdateMixin[AnalyticAccountModel],
    PaginationMixin[AnalyticAccountModel],
):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "analytic-accounts"
    model = AnalyticAccountModel

    def create(
        self, data, analytic_plan, client=None, params=None, client_request_id=None
    ):
        return super().create(
            data=data,
            client=client,
            params=params,
            client_request_id=client_request_id,
            extra_path=f"analytic-plans/{analytic_plan}",
        )

    def get(
        self, chift_id: str, analytic_plan: str, client=None, params=None
    ) -> AnalyticAccountModel:
        return super().get(
            chift_id=chift_id,
            client=client,
            params=params,
            extra_path=f"analytic-plans/{analytic_plan}",
        )

    def update(
        self,
        chift_id: str,
        analytic_plan: str,
        data,
        client=None,
        params=None,
        client_request_id=None,
    ):
        return super().update(
            chift_id=chift_id,
            data=data,
            client=client,
            params=params,
            client_request_id=client_request_id,
            extra_path=f"analytic-plans/{analytic_plan}",
        )


class Payable(
    ReadMixin[PayableModel],
    UpdateMixin[PayableModel],
    PaginationMixin[PayableModel],
):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "payables"
    model = PayableModel

    def mark_as_exported(self, chift_id: str, client=None, params=None):
        return super().update(
            chift_id=chift_id,
            data=None,
            client=client,
            params=params,
            extra_path="mark-as-exported",
        )


class FinancialMovement(
    UpdateMixin[FinancialMovementModel], PaginationMixin[FinancialMovementModel]
):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "financial-movements"
    model = FinancialMovementModel

    def mark_as_exported(self, chift_id: str, client=None, params=None):
        return super().update(
            chift_id=chift_id,
            data=None,
            client=client,
            params=params,
            extra_path="mark-as-exported",
        )


class Supplier(
    CreateMixin[SupplierModel],
    ReadMixin[SupplierModel],
    UpdateMixin[SupplierModel],
    PaginationMixin[SupplierModel],
):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "suppliers"
    model = SupplierModel


class Employee(PaginationMixin[EmployeeModel]):
    chift_vertical: ClassVar = "spend_management"
    chift_model: ClassVar = "employees"
    model = EmployeeModel
