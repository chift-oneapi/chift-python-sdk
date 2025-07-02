# Changelog

## 0.3.2 - 2025-07-02
* reset client_request_id and raw_data after a request

## 0.3.1 - 2025-06-22
* make sure pagination stops if list of items is empty

## 0.3.0 - 2025-06-18
* add possibility to iterate over pages when doing all requests instead of loading everything in memory
* improve typing on mixins concerning map_model and raw_data parameters
* update models (add create journal, create bank account, create ledger account)

## 0.2.0 - 2025-06-09
* remove raw-data and x-chift-client-requestid from headers on uncessary endpoints

## 0.1.99 - 2025-06-09
* allow to use x-chift-client-requestid header for Idempotency on create/update requests

## 0.1.98 - 2025-05-27
* allow to use raw_data parameter to get raw data from the API

## 0.1.97 - 2025-05-21
* add IssueLevel enum with "error" and "warning" values
* add "general_discount" option to POSLineItemType
* add `cost` field to ProductItemInput
* add `level` field to IssueItem model
* add `iban` field to Journal model
* fix multiple typos (sofware → software)
* update field types and descriptions
* change `account_number` in PMSCustomerItem from required to optional
* improve documentation for `account_info` and partner_info fields

## 0.1.96 - 2025-04-28
* fix models

## 0.1.95 - 2025-04-22
* migrate from pydantic.v1 BaseModel to pydantic.BaseModel
* added unit tests

## 0.1.94 - 2025-04-22
* update OpenAPI documentation

## 0.1.93 - 2025-04-19
* update `InvoicingPaymentItem` with optional fields: `payment_method_id`, `payment_method_name`, `invoice_id`, `invoice_number`

## 0.1.92 - 2025-04-18
* changed fields to optional `account_number`, `journal_id`, `journal_name`
* updated `integrationid` data type from `str` to `int`

## 0.1.91 - 2025-04-17
* fix float field in models

## 0.1.90 - 2025-04-16
* migrate to Pydantic 2.0

## 0.1.89 - 2025-04-15
* add route get taxes (PMS)

## 0.1.88 - 2025-04-01
* internal: add ignored error codes

## 0.1.87 - 2025-03-31
* ecommerce: add unit_cost to product variant

## 0.1.86 - 2025-03-20
* pos: improve closure model

## 0.1.85 - 2025-02-25
* accounting: add push attachment endpoint

## 0.1.84 - 2025-02-18
* pms: add get one customer endpoint

## 0.1.83 - 2025-02-10
* add support for specific header

## 0.1.82 - 2025-01-20
* invoicing: add italian specific fields

## 0.1.81 - 2025-01-13
* fix vat code models

## 0.1.80 - 2025-01-11
* invoicing: return exchange rate on invoices

## 0.1.79 - 2024-12-23
* accounting: add multiple matching endpoint

## 0.1.78 - 2024-12-20
* invoicing: fix invoicing router error

## 0.1.77 - 2024-12-20
* invoicing: add payments and payment methods

## 0.1.76 - 2024-12-10
* pos: add discount type

## 0.1.75 - 2024-12-01
* invoicing: add Italian specificities regarding e-Invoicing

## 0.1.74 - 2024-11-19
* pms: add customers route

## 0.1.73 - 2024-11-12
* pms: update model and add new route

## 0.1.72 - 2024-10-21
* sync: add update mixin for sync configuration modification

## 0.1.71 - 2024-10-01
* ecommerce: add tags on orders
* accounting: add account info when creation is required in the entry creation request

## 0.1.70 - 2024-10-01
* pos: add product type & menu_id

## 0.1.69 - 2024-09-22
* invoicing: add accounting date on invoices

## 0.1.68 - 2024-08-26
* payment: add endpoint for payment retrieval

## 0.1.67 - 2024-08-19
* accounting: add endpoint to match accounting entries
* custom: fix delete mixin
* ecommerce: add removed tag on fees

## 0.1.66 - 2024-08-17
* ecommerce: add returns on orders and current amounts

## 0.1.65 - 2024-08-02
* invoicing: add externa_reference on contacts

## 0.1.64 - 2024-07-09
* support test client

## 0.1.63 - 2024-06-30
* new field delivery_fee in POS model

## 0.1.62 - 2024-06-10
* connections: add delete endpoint

## 0.1.61 - 2024-05-31
* get integration: add post_connections

## 0.1.60 - 2024-05-26
* ecommerce: add creation date on transactions

## 0.1.59 - 2024-05-23
* POS: add new field 'guests'

## 0.1.58 - 2024-05-22
* pms: add PMS vertical

## 0.1.57 - 2024-05-22
* ecommerce: add transactions on refunds + new order status

## 0.1.56 - 2024-05-07
* ecommerce: add delivery date on orders

## 0.1.55 - 2024-04-11
* ecommerce: add product categories on order line items

## 0.1.54 - 2024-04-11
* ecommerce: add id on shipping refunds

## 0.1.53 - 2024-04-10
* ecommerce: add id on fees

## 0.1.52 - 2024-04-03
* fix issues connection creation

## 0.1.50 - 2024-04-03
* add endpoints to create connections and consumers

## 0.1.49 - 2024-03-26
* add countries endpoint in eCommerce

## 0.1.48 - 2024-03-13
* update connection model: add agent field

## 0.1.47 - 2024-03-13
* add challenge question in sync mapping model

## 0.1.46 - 2024-02-27
* add analytic accounts support in SDK (Accounting)

## 0.1.45 - 2024-02-26
* update POS model: description optional

## 0.1.44 - 2024-02-25
* update orders model (eCommerce): add discounts on fees

## 0.1.43 - 2024-02-17
* update models to support custom mappings

## 0.1.42 - 2024-02-16
* update orders model (eCommerce): multiple payment methods + transactions + creation date on each element of an order

## 0.1.41 - 2024-02-14
* update journal entries creation (Accounting): add possibility to create draft entries

## 0.1.40 - 2024-02-06
* update orders model (eCommerce): add gift card detail

## 0.1.39 - 2024-01-31
* update refunds model (eCommerce): add shipping details

## 0.1.38 - 2024-01-28
* update refunds model (eCommerce)

## 0.1.37 - 2024-01-25
* update accounting category model (POS)

## 0.1.36 - 2024-01-25
* add new POS route: Get accounting categories

## 0.1.34 & 0.1.35 - 2024-01-21
* fix delete requests response handling

## 0.1.33 - 2024-01-20
* new endpoint to delete datastoredata by id

## 0.1.32 - 2024-01-12
* update invoicing API: add custom get and update endpoints

## 0.1.31 - 2024-01-04
* update sync models due to update in mappings

## 0.1.30 - 2023-12-29
* update models + add endpoint: add categories and taxes to eCommerce

## 0.1.29 - 2023-12-19
* update models + add endpoint: add payment methods to eCommerce

## 0.1.28 - 2023-12-06
* update models: description of mappings is optional + multiple triggers on flows

## 0.1.27 - 2023-12-05
* fix custom API get one

## 0.1.26 - 2023-11-24
* New routes for POS: Get products & Get product categories

## 0.1.25 - 2023-11-16
* update models: add special AddressType for Invoicing API

## 0.1.24 - 2023-11-13
* update models: add cost and available_quantity on products in invoicing API

## 0.1.23 - 2023-11-07
* fix accounting/invoices params

## 0.1.22 - 2023-11-05
* add delete endpoint on custome API

## 0.1.21 - 2023-11-01
* add optional params on create and update endpoint

## 0.1.20 - 2023-10-12
* update models to have metadata

## 0.1.19 - 2023-10-12
* Retry: retry mechanism on 502 if 'max_retries' is passed to ChiftClient

## 0.1.18 - 2023-10-09
* Payment: add balances endpoints

## 0.1.17 - 2023-10-09
* Accounting: generic endpoint for entries creation

## 0.1.16 - 2023-10-05
* Errors: missing detail in error

## 0.1.15 - 2023-09-22
* Accounting: add outstandings, financial-entry endpoints

## 0.1.14 - 2023-09-22
* Invoicing: add support for custom endpoints

## 0.1.13 - 2023-09-19
* Invoicing: use model with pdf

## 0.1.12 - 2023-09-11
* Payment: add new types

## 0.1.11 - 2023-09-11
* Fixes + CI improvments

## 0.1.10 - 2023-09-08
* Fixes + models update

## 0.1.9 - 2023-08-29
* Payment: add new vertical

## 0.1.8 - 2023-08-22
* Sync,Data,Connection,Log direcly accessible from consumer

## 0.1.7 - 2023-08-18
* Ecommerce: add variants

## 0.1.6 - 2023-08-17
* Custom: support for custom endpoint added

## 0.1.5 - 2023-08-17
* models: bugfixes (optional id)

## 0.1.4 - 2023-08-16
* models: update (datastore)

## 0.1.3 - 2023-08-16
* Mixin: update

## 0.1.1 - 2023-08-01
* Accounting: add journal entries

## 0.1.0 - 2023-08-01
* First release
