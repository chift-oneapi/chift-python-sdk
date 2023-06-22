
We generate the models used in this SDK thanks to our openapi documentation with [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/)

```bash
datamodel-codegen --input ./openapi.json --output openapi.py
```

Then, those models are mapped to the one used in the python SDK in ```models.py```