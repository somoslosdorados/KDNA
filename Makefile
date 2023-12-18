.PHONY: install run

run:
	poetry run python kdna/main.py

clear:
	rm -Rf ./data/*
	echo "a very secret secret" > ./data/secret.txt
