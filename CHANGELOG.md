# Changelog

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
