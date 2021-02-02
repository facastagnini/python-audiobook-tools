PYTHON ?= python3

default: test

clean:
	@echo "[$@]"
	deactivate 2> /dev/null || true
	rm -rf .virtualenv nosetests.xml .noseids *.egg-info build

setup: virtualenv update_requirements
	@echo 'The python virtual environment has been setup, you have to activate it, execute: source .virtualenv/bin/activate'

virtualenv:
	@echo "[$@]"
	$(PYTHON) -m venv .virtualenv \
	&& ./.virtualenv/bin/pip install --upgrade pip-tools wheel \
	&& ./.virtualenv/bin/pip install --upgrade -r requirements-dev.txt \
	&& ./.virtualenv/bin/pip install --editable .
	@echo 'The python virtual environment has been setup, you have to activate it, execute: source .virtualenv/bin/activate'

update_requirements: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/pip-compile --upgrade requirements.in \
	&& ./.virtualenv/bin/pip-compile --upgrade requirements-dev.in \
	&& ./.virtualenv/bin/pip-sync requirements-dev.txt

test: isort auto_formatter_test lint unit_test 

isort: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/isort ./test ./audiobook_tools setup.py

# https://github.com/psf/black
auto_formatter_test: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/black --check --diff --color .

# https://github.com/psf/black
auto_formatter: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/black .

lint: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/flake8helled ./test ./audiobook_tools setup.py

# https://docs.python-guide.org/writing/tests/#unittest
unit_test: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/python -m pytest 

build: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/python setup.py sdist

# publish:
# 	@echo "[$@]"
# 	./.virtualenv/bin/python setup.py upload
