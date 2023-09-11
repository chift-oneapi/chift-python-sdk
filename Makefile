VENV_NAME?=venv

venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: setup.py
	python3 -m pip install --upgrade pip virtualenv
	@test -d $(VENV_NAME) || python3 -m virtualenv --clear $(VENV_NAME)
	${VENV_NAME}/bin/python -m pip install -e .[dev]
	@touch $(VENV_NAME)/bin/activate

test: venv
	@${VENV_NAME}/bin/python -m pytest --cov

fmt: venv
	@${VENV_NAME}/bin/python -m isort .
	@${VENV_NAME}/bin/python -m autoflake --remove-all-unused-imports --ignore-init-module-imports -r --in-place .
	@${VENV_NAME}/bin/python -m black ./

fmtcheck: venv
	@${VENV_NAME}/bin/python -m black ./ --check

coveralls: venv
	${VENV_NAME}/bin/python -m pip install -U coveralls
	${VENV_NAME}/bin/coveralls

clean:
	@rm -rf $(VENV_NAME) build/ dist/

publish: clean venv
	${VENV_NAME}/bin/python -m build
	${VENV_NAME}/bin/python -m twine check dist/*
	${VENV_NAME}/bin/python -m twine upload dist/*

.PHONY: venv test clean
