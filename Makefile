

.PHONY: all
all:
	flask --app app run --debug

.PHONY: lint
lint:
	ruff check --fix

.PHONY: fmt
fmt:
	ruff format

.PHONY: check
check:
	ruff check
	ruff format --diff

.PHONY: test
test:
	pytest
