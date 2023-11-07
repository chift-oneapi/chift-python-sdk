# Chift Python Library

[![pypi](https://img.shields.io/pypi/v/chift.svg)](https://pypi.python.org/pypi/chift)
[![Build Status](https://github.com/chift-oneapi/chift-python-sdk/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/chift-oneapi/chift-python-sdk/actions?query=branch:main)
[![Coverage Status](https://coveralls.io/repos/github/chift-oneapi/chift-python-sdk/badge.svg?branch=main)](https://coveralls.io/github/chift-oneapi/chift-python-sdk?branch=master)


The Chift Python library provides convenient access to the Chift API from
applications written in the Python language.

## Documentation

See the [API docs](https://chift.stoplight.io/docs/chift-api/intro).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install --upgrade chift
```

Install from source with:

```sh
python setup.py install
```

### Requirements

- Python 3.9+

## Usage

```python
import chift

chift.client_secret = "Spht8g8zMYWHTRaT1Qwy"
chift.client_id = "pZMQxOJJ6tl1716"
chift.account_id = "a8bfa890-e7ab-480f-9ae1-4c685f2a2a76"
chift.url_base = "http://chift.localhost:8000" # for development

# get a consumer
consumer = chift.Consumer.get("0e260397-997e-4791-a674-90ff6dab7caa")

# get all products
products = consumer.invoicing.Product.all(limit=2)

# get one products
product = consumer.invoicing.Product.get("PRD_3789488")

# print the product name
print(product.name)
```

## Development

Set up the development env:

```sh
make
```

Run all tests:

```sh
make test
```

Run the formatter:

```sh
make fmt
```
