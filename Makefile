.PHONY: setup clean update venv venv-run install run

PYENV:=$(shell which pyenv)
SHELL:=/bin/bash
VIRTUAL_ENV:=env

setup: clean update venv

clean:
	@echo [make clean]: Started
	@rm -rf env 2>/dev/null
	@rm -rf WhatToPlay/__pycache__ 2>/dev/null
	@echo [make clean]: Finished

update:
	@echo [make update]: Started
	@git checkout main
	@git pull
	@echo [make update]: Finished

venv:
	@echo [make venv]: Started
ifdef PYENV
	@echo [make venv]: pyenv found at "$(PYENV)"
	@$(PYENV) exec python -m pip install --upgrade pip
	@$(PYENV) exec python -m pip install virtualenv
	@$(PYENV) exec virtualenv $(VIRTUAL_ENV)
	@echo [make venv]: Finished
else
	@echo [make venv]: pyenv could not be found
	@echo [make venv]: Failed
endif

# Run this via "source env/bin/activate && make venv-run; deactivate && make clean"

venv-run: install run

install:
	@echo [make install]: Started
ifdef PYENV
	@echo [make install]: pyenv found at "$(PYENV)"
	@$(PYENV) exec pip install -r requirements.txt
	@echo [make install]: Finished
else
	@echo [make install]: pyenv could not be found
	@echo [make install]: Failed
endif

run:
	@echo [make run]: Started
ifdef PYENV
	@echo [make run]: pyenv found at "$(PYENV)"
	@$(PYENV) exec python -m WhatToPlay
	@echo [make run]: Finished
else
	@echo [make run]: pyenv could not be found
	@echo [make run]: Failed
endif
