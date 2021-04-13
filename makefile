.PHONY := install, install-prod, help, ui, clean, clean-ui
.DEFAULT_GOAL := install

INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

BUILD_DIR := ui
SRC_DIR := ui-src

UIS := $(shell find $(SRC_DIR) -name *.ui)
UIPYS := $(UIS:$(SRC_DIR)/%.ui=$(BUILD_DIR)/%.py)

tools:
	@python -m pip -q install pip-tools

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.%.txt: requirements.%.in
	@echo "Builing $@"
	@pip-compile -q -o $@ $^

requirements.txt: setup.py
	@echo "Builing $@"
	@pip-compile -q $^
	@sed -i 's/pip-compile $^/pip-compile/g' $@

install-prod: requirements.txt ## Install production requirements
	@echo "Installing $^"
	@pip-sync $^

install: requirements.txt $(REQS) ## Install development requirements (default)
	@echo "Installing $^"
	@pip-sync $^

$(BUILD_DIR)/%.py: $(SRC_DIR)/%.ui
	pyuic5 $^ -o $@

ui: $(UIPYS) ## Build the python file for the UI

clean-ui:
	@rm -f $(UIPYS)

clean: ## Clean temporary files
	@find . -type f -name '*.pyc' -exec rm -f {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@rm -rf *.egg-info
	@find . -maxdepth 1 -type d -name results-* -exec rm -rf {} \;
