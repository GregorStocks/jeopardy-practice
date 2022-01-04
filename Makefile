SHELL := /bin/bash

.PHONY: clean freeze run black curl

venv: requirements.txt
	rm -rf venv
	virtualenv -p /usr/bin/python3.9 venv
	source venv/bin/activate && pip install -r requirements.txt

freeze:
	source venv/bin/activate && pip freeze > requirements.txt

clean:
	rm -rf venv

black:
	source venv/bin/activate && black api/

run: venv
	source venv/bin/activate && python api/main.py

curl:
	curl 'http://localhost:5000/graphql' -H "Content-type: application/json" -XPOST --data-raw '{"query":"{ hello }","variables": {}}'
