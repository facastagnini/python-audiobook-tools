PYTHON ?= python3
PYTHON_ENV_PATH ?= .virtualenv

.PHONY: default
default: isort auto_formatter test

.PHONY: git/clean
git/clean:
	@echo "[$@]"
	@# generic cleanup task
	@# remove untracked files and directories explicitly ignored by .gitignore
	-git clean -dX --interactive

.PHONY: clean
clean:
	@echo "[$@]"
	-rm -rf .virtualenv nosetests.xml .noseids *.egg-info build

.PHONY: setup
setup: $(PYTHON_ENV_PATH) update_requirements
	@echo "The python virtual environment has been setup, you have to activate \
	it, execute: source $(PYTHON_ENV_PATH)/bin/activate"

$(PYTHON_ENV_PATH):
	@echo "[$@]"
	$(PYTHON) -m venv $(PYTHON_ENV_PATH) \
	&& ./$(PYTHON_ENV_PATH)/bin/pip install --upgrade -r requirements-dev.txt \
	&& ./$(PYTHON_ENV_PATH)/bin/pip install --editable .
	@echo "The python virtual environment has been setup, you have to activate \
	it, execute: source $(PYTHON_ENV_PATH)/bin/activate"

.PHONY: update_requirements
update_requirements: $(PYTHON_ENV_PATH)
	@echo "[$@]"
	./$(PYTHON_ENV_PATH)/bin/pip-compile    --upgrade requirements.in \
	&& ./$(PYTHON_ENV_PATH)/bin/pip-compile --upgrade requirements-dev.in \
	&& ./$(PYTHON_ENV_PATH)/bin/pip-sync requirements-dev.txt

.PHONY: test
test: auto_formatter_test lint unit_test

# https://github.com/psf/black
.PHONY: auto_formatter_test
auto_formatter_test: $(PYTHON_ENV_PATH)
	@echo "[$@]"
	./$(PYTHON_ENV_PATH)/bin/black --check --diff --color .

.PHONY: lint
lint: $(PYTHON_ENV_PATH)
	@echo "[$@]"
	./$(PYTHON_ENV_PATH)/bin/flake8helled ./tests ./audiobook_tools setup.py

# https://docs.python-guide.org/writing/tests/#unittest
.PHONY: unit_test
unit_test: $(PYTHON_ENV_PATH)
	@echo "[$@]"
	./$(PYTHON_ENV_PATH)/bin/python -m pytest

# https://github.com/psf/black
.PHONY: auto_formatter
auto_formatter: $(PYTHON_ENV_PATH)
	@echo "[$@]"
	./$(PYTHON_ENV_PATH)/bin/black .

.PHONY: isort
isort: $(PYTHON_ENV_PATH)
	@echo "[$@]"
	./$(PYTHON_ENV_PATH)/bin/isort ./tests ./audiobook_tools setup.py

.PHONY: build
build: $(PYTHON_ENV_PATH)
	@echo "[$@]"
	./$(PYTHON_ENV_PATH)/bin/python setup.py sdist

# publish:
# 	@echo "[$@]"
# 	./.virtualenv/bin/python setup.py upload
