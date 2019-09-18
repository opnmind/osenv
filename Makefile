.PHONY: clean build sdist test tox lint

.ONESHELL:
help:
	@echo "help"

clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./*.egg-info
	rm -rf ./.tox
	rm -f ./.ostackrc.enc
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

install:
	pip install -e .

build:
	python setup.py -q sdist bdist_wheel

sdist:
	python setup.py sdist

test: unittest flake8

unittest:
	python -m unittest discover -v

flake8:
	flake8 --exit-zero lib/ tests/ osenv setup.py

flake8-stats:
	flake8 --count --statistics --exit-zero lib/ tests/ osenv setup.py

tox: clean
	clear && tox

format_black:
	black lib/ tests/ osenv setup.py

coverage:
	pytest --cov=lib tests/
