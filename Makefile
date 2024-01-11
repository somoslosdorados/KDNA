.PHONY: install run

run:
	poetry run python kdna/main.py

test:
	poetry run pytest tests

clear:
	rm -Rf ./data/*
	echo "a very secret secret" > ./data/secret.txt
