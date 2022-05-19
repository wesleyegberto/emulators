run:
	python3 ./src/main.py

tests:
	python3 -m unittest discover -vs test -p "*_test.py"

coverage:
	coverage run --source=src/ -m pytest test/
	coverage report -m
	coverage xml -i

