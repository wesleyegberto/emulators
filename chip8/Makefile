run:
	python3 ./src/main.py

env:
	python3 -m venv .penv/

deps:
	pip3 install -r requirements.txt

tests:
	python3 -m unittest discover -vs test -p "*_test.py"

pytest:
	python3 -m pytest -vs test/

coverage:
	python3 -m pytest -vs test/ --cov=src/ --cov-report=term --cov-report=html

