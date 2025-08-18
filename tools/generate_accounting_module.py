from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel

from tools.model_generator import (
    ArgumentSpec,
    BaseClassSpec,
    ClassSpec,
    ClassVarSpec,
    FunctionBody,
    FunctionSpec,
    ModelGenerator,
    TypeExpression,
)

"""
Generate an accounting client module at the repository root using tools.model_generator.

This generator dynamically reads the OpenAPI JSON file and creates classes based on
actual API endpoints under the /consumers/{consumer_id}/accounting/* namespace.
"""


class EndpointInfo:
    """Information about a single API endpoint."""

    def __init__(self, path: str, method: str, operation_data: dict):
        self.path = path
        self.method = method.upper()
        self.operation_data = operation_data
        self.path_without_params = self._extract_base_path(path)
        self.params = self._parse_parameters(operation_data.get("parameters", []))

    def _extract_base_path(self, path: str) -> str:
        """Extract the base path without dynamic segments."""
        # Remove /consumers/{consumer_id}/accounting/ prefix
        if path.startswith("/consumers/{consumer_id}/accounting/"):
            base = path[len("/consumers/{consumer_id}/accounting/") :]
            # Remove path parameters like /{id}, /{invoice_id}, etc.
            base = re.sub(r"\/\{[^}]+\}", "", base)
            return base
        return path

    def _parse_parameters(self, parameters_data: dict) -> List[EndpointParameter]:
        """Parse a list of parameters into a list of EndpointParameter objects."""
        params = []
        for param in parameters_data:
            if param.get("name") != "consumer_id":
                params.append(self._parse_parameter(param))
        return params

    def _parse_parameter(self, param_spec: Dict[str, Any]) -> EndpointParameter:
        """Parse a parameter specification into a PathParameter object."""
        schema = param_spec.get("schema", {})

        # Handle $ref in schema
        ref = schema.get("$ref")
        if ref:
            return EndpointParameter(
                name=param_spec["name"],
                type="ref",
                ref=ref,
                description=param_spec.get("description"),
                title=schema.get("title", param_spec["name"]),
                required=param_spec.get("required", False),
                param_in=param_spec.get("in", "path"),
            )

        # Handle regular schema types
        param_type = schema.get("type", "string")
        param_format = schema.get("format")
        enum_values = schema.get("enum")

        return EndpointParameter(
            name=param_spec["name"],
            type=param_type,
            format=param_format,
            description=param_spec.get("description"),
            title=schema.get("title", param_spec["name"]),
            required=param_spec.get("required", False),
            enum_values=enum_values,
            param_in=param_spec.get("in", "path"),
        )

    def get_resource_name(self) -> str:
        """Get a reasonable class name for this resource."""
        base = self.path_without_params
        # Convert kebab-case to PascalCase
        parts = base.split("/")
        name_parts = []
        for part in parts[:2]:
            if part:
                # Convert kebab-case to PascalCase
                words = part.split("-")
                name_parts.append("".join(word.capitalize() for word in words))
        return "".join(name_parts)


class EndpointParameter(BaseModel):
    """Represents a path parameter from the OpenAPI spec."""

    name: str
    type: str
    format: Optional[str] = None
    description: Optional[str] = None
    title: Optional[str] = None
    required: bool = True
    enum_values: Optional[List[str]] = None
    ref: Optional[str] = None
    param_in: Literal["path", "query"]

    def get_python_type(self) -> str:
        """Convert OpenAPI parameter type to Python type annotation."""
        if self.ref:
            # Extract the model name from the $ref
            ref_parts = self.ref.split("/")
            return ref_parts[-1] if ref_parts else "Any"

        type_mapping = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "List[str]",  # Simplified, could be more complex
            "object": "Dict[str, Any]",
        }

        base_type = type_mapping.get(self.type)

        if base_type is None:
            raise ValueError(f"Unknown type: {self.type}")

        # Handle UUID format
        if self.format == "uuid":
            return "UUID"
        elif self.format == "date":
            return "date"
        elif self.format == "date-time":
            return "datetime"

        # Handle enums
        if self.enum_values:
            return "str"  # Could create specific enum classes

        return base_type


class OpenApiParser:
    """Parses OpenAPI JSON to extract accounting endpoints."""

    def __init__(self, openapi_path: str):
        with open(openapi_path, "r") as f:
            self.spec = json.load(f)

    def get_accounting_endpoints(self) -> List[EndpointInfo]:
        """Extract all accounting endpoints from the OpenAPI spec."""
        endpoints = []
        paths = self.spec.get("paths", {})

        for path, methods in paths.items():
            if path.startswith("/consumers/{consumer_id}/accounting/"):
                for method, operation in methods.items():
                    if method.lower() in ["get", "post", "put", "patch", "delete"]:
                        endpoints.append(EndpointInfo(path, method, operation))

        return endpoints

    def group_endpoints_by_resource(
        self, endpoints: List[EndpointInfo]
    ) -> Dict[str, List[EndpointInfo]]:
        """Group endpoints by their resource name."""
        groups = {}
        for endpoint in endpoints:
            resource_name = endpoint.get_resource_name()
            if not resource_name:
                continue
            if resource_name not in groups:
                groups[resource_name] = []
            groups[resource_name].append(endpoint)
        return groups


class ModelMapper:
    """Maps OpenAPI response schemas to Python model classes."""

    # Known model mappings from the existing code
    MODEL_MAPPINGS = {
        "AnalyticPlanItem": "AnalyticPlanModel",
        "AnalyticAccountItemOutMultiAnalyticPlans": "AnalyticAccountMultiPlanModel",
        "AccountingVatCode": "TaxAccountingModel",
        "MiscellaneousOperationOut": "MiscellaneousOperationModel",
        "AccountItem": "AccountModel",
        "SupplierItemOut": "SupplierModel",
        "ClientItemOut": "ClientModel",
        "InvoiceItemOutMonoAnalyticPlan": "InvoiceAccountingModel",
        "InvoiceItemOutMultiAnalyticPlans": "InvoiceMultiPlanAccountingModel",
        "JournalEntryMultiAnalyticPlan": "JournalEntryModel",
        "FinancialEntryItemOut": "FinancialEntryModel",
        "OutstandingItem": "OutstandingModel",
        "Journal": "JournalModel",
        "MatchingOut": "MatchingModel",
        "MultipleMatchingOut": "MultipleMatchingModel",
        "EmployeeItem": "EmployeeModel",
        "AttachmentItemOut": "AttachmentModel",
        "BankAccountItemOut": "BankAccountModel",
        "AccountBalance": "AccountBalanceModel",
        "Payment": "AccountingPayment",
    }

    def get_model_for_endpoint(self, endpoint: EndpointInfo) -> str:
        """Determine the appropriate model class for an endpoint."""
        # Try to extract from response schema
        response_schema = self._get_response_schema(endpoint)
        if response_schema:
            return response_schema

        # Fallback to resource-based naming
        return f"{endpoint.get_resource_name()}Model"

    def _get_response_schema(self, endpoint: EndpointInfo) -> Optional[str]:
        """Extract the response schema name from the endpoint."""
        responses = endpoint.operation_data.get("responses", {})
        success_response = responses.get("200") or responses.get("201")
        if not success_response:
            return None

        content = success_response.get("content", {})
        json_content = content.get("application/json", {})
        schema = json_content.get("schema", {})

        # Handle array responses
        if schema.get("type") == "array":
            items = schema.get("items", {})
            ref = items.get("$ref")
        else:
            ref = schema.get("$ref")

        if ref and ref.startswith("#/components/schemas/"):
            return ref.split("/")[-1].replace("_", "")
        return None


class MixinMapper:
    """Maps HTTP methods and endpoint patterns to appropriate mixins."""

    def get_mixins_for_resource(
        self, endpoints: List[EndpointInfo]
    ) -> List[Tuple[str, str]]:
        """Determine which mixins a resource should inherit from."""
        mixins = []
        model_name = None

        # Determine the model name (should be consistent across endpoints)
        mapper = ModelMapper()
        for endpoint in endpoints:
            if not model_name:
                model_name = mapper.get_model_for_endpoint(endpoint)

        # Ensure we have a model name
        if not model_name:
            model_name = (
                f"{endpoints[0].get_resource_name()}Model"
                if endpoints
                else "UnknownModel"
            )

        methods = set(ep.method for ep in endpoints)

        # Map methods to mixins
        if "POST" in methods:
            mixins.append(("CreateMixin", model_name))
        if "GET" in methods:
            # Check if it's a list endpoint or single item
            has_list = any(  # TODO Find correct way to map
                not ep.params
                or len([p for p in ep.params if "id" in p.name.lower()]) == 0
                for ep in endpoints
                if ep.method == "GET"
            )
            has_single = any(
                ep.params and any("id" in p.name.lower() for p in ep.params)
                for ep in endpoints
                if ep.method == "GET"
            )

            if has_single:
                mixins.append(("ReadMixin", model_name))
            if has_list:
                mixins.append(("PaginationMixin", model_name))
        if "PATCH" in methods or "PUT" in methods:
            mixins.append(("UpdateMixin", model_name))
        if "DELETE" in methods:
            mixins.append(("DeleteMixin", model_name))

        return mixins or [("PaginationMixin", model_name)]  # Default fallback


class DynamicClassGenerator:
    """Generates classes dynamically based on OpenAPI endpoints."""

    def __init__(self, generator: ModelGenerator):
        self.gen = generator
        self.model_mapper = ModelMapper()
        self.mixin_mapper = MixinMapper()
        self.imported_models = set()
        self._add_imports()

    def _add_imports(self):
        """Add common imports needed by all generated classes."""
        self.gen.add_import("typing", "ClassVar")
        self.gen.add_import("chift.api.mixins", "CreateMixin")
        self.gen.add_import("chift.api.mixins", "DeleteMixin")
        self.gen.add_import("chift.api.mixins", "PaginationMixin")
        self.gen.add_import("chift.api.mixins", "ReadMixin")
        self.gen.add_import("chift.api.mixins", "UpdateMixin")

    def get_model_path(self, endpoints: List[EndpointInfo]) -> str:
        """Extract the model path from endpoint patterns."""
        # Use the most common base path
        paths = [ep.path_without_params for ep in endpoints]
        if not paths:
            return "unknown"
        return max(set(paths), key=paths.count)

    def needs_special_handling(
        self, resource_name: str, endpoints: List[EndpointInfo]
    ) -> bool:
        """Check if this resource needs special method implementations."""
        # Resources with path parameters often need special handling
        has_path_params = any(
            len(ep.params) > 0 and any(p.param_in == "path" for p in ep.params)
            for ep in endpoints
        )
        # Resources with type-based paths need special handling
        # has_type_path = any("type" in ep.path for ep in endpoints)
        # # Multi-analytic-plans paths need special handling
        # has_multi_analytic = any("multi-analytic-plans" in ep.path for ep in endpoints)

        return has_path_params

    def generate_class(
        self, resource_name: str, endpoints: List[EndpointInfo]
    ) -> ClassSpec:
        """Generate a class for a resource based on its endpoints."""
        mixins = self.mixin_mapper.get_mixins_for_resource(endpoints)
        model_path = self.get_model_path(endpoints)

        # Create base class specifications
        base_specs = []
        for mixin_name, model_name in mixins:
            if model_name and model_name != "None":
                self.ensure_model_imported(model_name)
                base_specs.append(
                    BaseClassSpec(
                        TypeExpression(mixin_name, (TypeExpression(model_name),))
                    )
                )
            else:
                base_specs.append(BaseClassSpec(TypeExpression(mixin_name, ())))

        # Create the class
        cls = self.gen.new_class(name=resource_name, bases=base_specs)

        # Add class variables
        cls.class_vars.append(
            ClassVarSpec(
                name="chift_vertical",
                type_hint=TypeExpression("str"),
                value="accounting",
            )
        )
        cls.class_vars.append(
            ClassVarSpec(
                name="chift_model", type_hint=TypeExpression("str"), value=model_path
            )
        )

        # Add model attribute if we have a model
        if mixins and mixins[0][1] and mixins[0][1] != "None":
            cls.class_vars.append(ClassVarSpec(name="model", value=mixins[0][1]))

        # Add special methods if needed
        if self.needs_special_handling(resource_name, endpoints):
            self.add_special_methods(cls, resource_name, endpoints)

        return cls

    def add_special_methods(
        self, cls: ClassSpec, resource_name: str, endpoints: List[EndpointInfo]
    ):
        """Add special method implementations for complex endpoints."""
        # Handle invoice type-based endpoints
        if any("type" in ep.path for ep in endpoints):
            self.add_typed_all_method(cls)

        # Handle multi-analytic-plans endpoints
        if any("multi-analytic-plans" in ep.path for ep in endpoints):
            self.add_multi_analytic_methods(cls)

        # Handle custom endpoints
        if resource_name == "Custom":
            self.add_custom_methods(cls)

        # Handle attachment-specific endpoints
        if resource_name == "Attachments" and any("pdf" in ep.path for ep in endpoints):
            self.add_attachment_methods(cls)

    def add_typed_all_method(self, cls: ClassSpec):
        """Add an all() method that requires an invoice_type parameter."""
        all_fn = FunctionSpec(
            name="all",
            arguments=[
                ArgumentSpec(name="invoice_type"),
                ArgumentSpec(name="params", default=None),
                ArgumentSpec(name="client", default=None),
                ArgumentSpec(name="limit", default=None),
            ],
        )
        body = FunctionBody()
        body.add_line('self.extra_path = f"type/{invoice_type}"')
        body.add_line("return super().all(params=params, limit=limit, client=client)")
        all_fn.body = body
        cls.methods.append(all_fn)

    def add_multi_analytic_methods(self, cls: ClassSpec):
        """Add methods for multi-analytic-plans endpoints."""
        # Override create method
        create_fn = FunctionSpec(
            name="create",
            arguments=[
                ArgumentSpec(name="data"),
                ArgumentSpec(name="analytic_plan"),
                ArgumentSpec(name="client", default=None),
                ArgumentSpec(name="params", default=None),
                ArgumentSpec(name="client_request_id", default=None),
            ],
        )
        body = FunctionBody()
        body.add_line('self.extra_path = f"multi-analytic-plans/{analytic_plan}"')
        body.add_line("return super().create(data=data, client=client, params=params)")
        create_fn.body = body
        cls.methods.append(create_fn)

        # Override get method
        get_fn = FunctionSpec(
            name="get",
            arguments=[
                ArgumentSpec(name="chift_id", type_hint=TypeExpression("str")),
                ArgumentSpec(name="analytic_plan", type_hint=TypeExpression("str")),
                ArgumentSpec(name="client", default=None),
                ArgumentSpec(name="params", default=None),
            ],
        )
        body = FunctionBody()
        body.add_line('self.extra_path = f"multi-analytic-plans/{analytic_plan}"')
        body.add_line(
            "return super().get(chift_id=chift_id, client=client, params=params)"
        )
        get_fn.body = body
        cls.methods.append(get_fn)

    def add_custom_methods(self, cls: ClassSpec):
        """Add methods for custom endpoints that accept dynamic paths."""
        methods_to_add = ["all", "create", "get", "update", "delete"]

        for method_name in methods_to_add:
            if method_name == "all":
                fn = FunctionSpec(
                    name="all",
                    arguments=[
                        ArgumentSpec(name="custom_path"),
                        ArgumentSpec(name="params", default=None),
                        ArgumentSpec(name="client", default=None),
                        ArgumentSpec(name="limit", default=None),
                    ],
                )
                body = FunctionBody()
                body.add_line("self.extra_path = custom_path")
                body.add_line(
                    "return super().all(params=params, map_model=False, client=client, limit=limit)"
                )
            elif method_name == "create":
                fn = FunctionSpec(
                    name="create",
                    arguments=[
                        ArgumentSpec(name="custom_path"),
                        ArgumentSpec(name="data"),
                        ArgumentSpec(name="client", default=None),
                        ArgumentSpec(name="params", default=None),
                    ],
                )
                body = FunctionBody()
                body.add_line("self.extra_path = custom_path")
                body.add_line(
                    "return super().create(data, map_model=False, client=client, params=params)"
                )
            else:
                continue  # Skip other methods for now

            fn.body = body
            cls.methods.append(fn)

    def add_attachment_methods(self, cls: ClassSpec):
        """Add special create method for attachment/PDF endpoints."""
        create_fn = FunctionSpec(
            name="create",
            arguments=[
                ArgumentSpec(name="invoice_id"),
                ArgumentSpec(name="data"),
                ArgumentSpec(name="client", default=None),
                ArgumentSpec(name="params", default=None),
            ],
        )
        body = FunctionBody()
        body.add_line('self.chift_model = "invoices"')
        body.add_line('self.extra_path = f"pdf/{invoice_id}"')
        body.add_line(
            "return super().create(data=data, client=client, params=params, map_model=False)"
        )
        create_fn.body = body
        cls.methods.append(create_fn)

    def ensure_model_imported(self, model_name: str):
        """Ensure a model is imported from chift.openapi.openapi."""
        if model_name not in self.imported_models:
            self.gen.add_import("chift.openapi.openapi", model_name)
            self.imported_models.add(model_name)

    def create_router_class(self, resource_names: List[str]) -> ClassSpec:
        """Create the main router class that instantiates all resource classes."""
        cls = ClassSpec(name="AccountingRouter")

        init_fn = FunctionSpec(name="__init__")
        init_fn.arguments.append(ArgumentSpec(name="consumer_id"))
        init_fn.arguments.append(ArgumentSpec(name="connection_id"))

        body = FunctionBody()
        for resource_name in sorted(resource_names):
            body.add_line(
                f"self.{resource_name} = {resource_name}(consumer_id, connection_id)"
            )

        init_fn.body = body
        cls.methods.append(init_fn)
        return cls


def main() -> None:
    # Initialize the generator
    gen = ModelGenerator(
        module_docstring=(
            "This file is auto-generated dynamically from the OpenAPI specification.\n\n"
            "Resources reflect only the /consumers/{{consumer_id}}/accounting/* endpoints."
        )
    )

    # Parse OpenAPI spec
    openapi_path = Path(__file__).parent.parent / "chift" / "openapi" / "openapi.json"
    parser = OpenApiParser(str(openapi_path))
    endpoints = parser.get_accounting_endpoints()

    if not endpoints:
        print("No accounting endpoints found in OpenAPI spec")
        return

    # Group endpoints by resource
    resource_groups = parser.group_endpoints_by_resource(endpoints)

    print(
        f"Found {len(endpoints)} accounting endpoints in {len(resource_groups)} resource groups"
    )
    for resource_name, eps in resource_groups.items():
        print(f"  {resource_name}: {len(eps)} endpoints")

    # Generate classes
    class_gen = DynamicClassGenerator(gen)

    resource_names = []
    for resource_name, resource_endpoints in resource_groups.items():
        if resource_name:  # Skip empty resource names
            class_gen.generate_class(resource_name, resource_endpoints)
            resource_names.append(resource_name)

    # Add router class
    router_cls = class_gen.create_router_class(resource_names)
    gen.add_class(router_cls)

    # Write output
    gen.write_to_path("generated_accounting.py")
    print("Generated accounting module: generated_accounting.py")


if __name__ == "__main__":
    main()
