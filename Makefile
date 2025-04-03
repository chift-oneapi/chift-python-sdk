.PHONY: install config test fmt fmtcheck coveralls clean publish

config:
	@poetry config virtualenvs.in-project true --local

install: config
	@poetry install --no-interaction

test: install
	@poetry run python -m pytest --cov

fmt: install
	@poetry run python -m isort .
	@poetry run python -m autoflake --remove-all-unused-imports --ignore-init-module-imports -r --in-place .
	@poetry run python -m black ./

fmtcheck: install
	@poetry run python -m black ./ --check

coveralls: install
	@poetry run pip install -U coveralls
	@poetry run python -m coveralls

clean:
	@rm -rf build/ dist/ .coverage .pytest_cache .venv
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +

publish: clean install
	@poetry build
	@poetry run python -m twine check dist/*
	@poetry run python -m twine upload dist/*