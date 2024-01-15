.PHONY: install run test clear

run:
	poetry run python kdna/__main__.py

test:
	poetry run pytest tests

clear:
	rm -Rf ./data/*
	echo "a very secret secret" > ./data/secret.txt
