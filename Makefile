SHELL := /bin/bash

.PHONY: clean freeze run black curl psql parse autogenerate upgrade serve cli venv

venv:
	rm -rf venv
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

freeze:
	source venv/bin/activate && pip freeze > requirements.txt

clean:
	rm -rf venv

black: venv
	source venv/bin/activate && black api/ alembic/ scripts/ cli/

serve: venv
	source venv/bin/activate && PYTHONPATH=. python api/main.py

curl:
	curl 'http://localhost:5000/graphql' -H "Content-type: application/json" -XPOST --data-raw '{"query":"{ numGames }","variables": {}}'; echo
	curl 'http://localhost:5000/graphql' -H "Content-type: application/json" -XPOST --data-raw '{"query":"mutation { ping(x:\"pong\") { ping } }","variables": {}}'; echo

upgrade: venv
	source venv/bin/activate && alembic upgrade head

autogenerate: venv
	read -p "Revision name:" REVISIONNAME; source venv/bin/activate && PYTHONPATH=. alembic revision --autogenerate -m "$$REVISIONNAME" ; black alembic

parse: venv
	source venv/bin/activate && scripts/parser.py

psql:
	PGPASSWORD=jeopardypassword psql -U jeopardy -d jeopardy

cli:
	source venv/bin/activate && cli/main.py

type:
	source venv/bin/activate && pyright cli/
