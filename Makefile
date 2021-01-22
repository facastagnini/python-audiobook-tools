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

test: auto_formatter_test lint unit_test 

# https://github.com/psf/black
auto_formatter_test:
	@echo "[$@]"
	# The GitHub editor is 127 chars wide
	./.virtualenv/bin/black --line-length 127 --check --diff --color .

# https://github.com/psf/black
auto_formatter:
	@echo "[$@]"
	# The GitHub editor is 127 chars wide
	./.virtualenv/bin/black --line-length 127 .

lint: virtualenv
	@echo "[$@]"
	# stop the build if there are Python syntax errors or undefined names
	./.virtualenv/bin/flake8 --count --select=E9,F63,F7,F82 --show-source --statistics ./tests ./audiobook_tools setup.py
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	./.virtualenv/bin/flake8 --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics ./tests ./audiobook_tools setup.py

# https://docs.python-guide.org/writing/tests/#unittest
unit_test: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/python setup.py nosetests
	# ./.virtualenv/bin/nosetests

# https://docs.python-guide.org/writing/tests/#doctest
doctest: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/python doctest

build: virtualenv
	@echo "[$@]"
	./.virtualenv/bin/python setup.py sdist

# publish:
# 	@echo "[$@]"
# 	./.virtualenv/bin/python setup.py upload
