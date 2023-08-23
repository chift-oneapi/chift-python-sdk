
# Development

## A model is changed in chift

As models are kept in sync thanks to openapi, you need to regenerate `openapi.py` and make sure there is no link error in `models.py`.

We generate the models used in this SDK thanks to  [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/)

```bash
datamodel-codegen --input ./openapi.json --output openapi.py
```

Then, those models are mapped to the one used in the python SDK in ```models.py```


## A route is added in chift

If there is a new route, here are the needed changes:

- Generate the new model in `openapi.py` thanks to an update in `openapi.json` and `datamodel-codegen`
- Create the link to openapi models and models used in this SDK in `models.py`
- Add the model to the relevant folder in `/models`
- Add the relevant mixins (create, update, list, read,...)
- Add tests for the model in `/tests`


## A route is changed in chift

- Find the exising model under `/models` and update its definition
