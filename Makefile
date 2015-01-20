.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "local_tests - run only the unit tests"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "sdist - source distribution"
	@echo "install - install package"
	@echo "install-deps-dev - install requirements from requirements-dev.txt"
	@echo "install-deps-production - install requirements from requirements.txt"


clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 HBaseBoard tests

test: install
	py.test --tb=short -s

local_test: install
	py.test --tb=short -s -m local_test

test-all:
	tox

coverage:
	coverage run --source HBaseBoard setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/HBaseBoard.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ HBaseBoard
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload


sdist: clean install-deps-production
	python setup.py sdist

dist: clean install-deps-production
	python setup.py bdist_wheel --universal
	ls -l dist

install-deps-dev: requirements.txt requirements-dev.txt
	pip install -r requirements-dev.txt

install-deps-production: requirements.txt
	pip install -r requirements.txt

install: clean dist
	rm -fr build/
	pip install dist/*.whl
