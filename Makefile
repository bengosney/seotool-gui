.PHONY: help clean test install all init dev css watch
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

HOOKS=$(.git/hooks/pre-commit)
INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml:
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/a7972e894720be19359ec846755131e248f8d281/.pre-commit-config.yaml > $@
	python -m pip install pre-commit
	pre-commit autoupdate

requirements.%.in:
	echo "-c requirements.txt" > $@

requirements.in:
	@touch $@

requirements.%.txt: requirements.%.in requirements.txt
	@echo "Builing $@"
	@python -m piptools compile -q -o $@ $^

requirements.txt: requirements.in
	@echo "Builing $@"
	@python -m piptools compile -q $^

.direnv: .envrc
	python -m pip install --upgrade pip
	python -m pip install wheel pip-tools
	@touch $@ $^

.git/hooks/pre-commit: .pre-commit-config.yaml
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.10" > $@
	@touch -d '+1 minute' $@
	@false

init: .direnv .git .git/hooks/pre-commit requirements.dev.txt ## Initalise a enviroment

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata
	rm -rf .mypy_cache
	rm -rf .hypothesis

install: requirements.txt $(REQS)
	@echo "Installing $^"
	@python -m piptools sync $^

_upgrade: requirements.in
	@echo "Upgrading pip packages"
	@python -m piptools compile -q --upgrade requirements.in

upgrade: _upgrade install
