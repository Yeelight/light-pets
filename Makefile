PYTHON ?= python3

.PHONY: build validate smoke

build:
	$(PYTHON) scripts/build_project.py

validate:
	$(PYTHON) scripts/validate_project.py

smoke: build validate
