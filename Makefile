SHELL := /bin/bash

.PHONY: clean freeze run black curl psql parse autogenerate upgrade serve cli

# Initial setup
venv:
	rm -rf venv
	/usr/bin/env python3.11 -m venv venv
	source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

upgrade: venv
	source venv/bin/activate && alembic upgrade head

clean:
	rm -rf venv

# Occasional env changes
freeze:
	source venv/bin/activate && pip freeze > requirements.txt

migration: venv
	read -p "Revision name:" REVISIONNAME; source venv/bin/activate && PYTHONPATH=. alembic revision -m "$$REVISIONNAME" ; black alembic

# Run once
parse: venv
	source venv/bin/activate && scripts/parser.py

download: venv
	mkdir -p data/j-archive
	source venv/bin/activate && scripts/download.py

# General purpose
black: venv
	source venv/bin/activate && black api/ alembic/ scripts/ cli/

psql:
	PGPASSWORD=jeopardypassword psql -U jeopardy -d jeopardy

# Main
cli: venv
	source venv/bin/activate && cli/main.py

