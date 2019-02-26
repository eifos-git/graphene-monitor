.PHONY: clean-pyc clean-build docs

clean: clean-build clean-pyc

clean-build:
	rm -fr build/ dist/ *.egg-info .eggs/ .tox/ __pycache__/ .cache/ .coverage htmlcov src

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	black monitor/

test:
	python3 setup.py test

build:
	python3 setup.py build

install: build
	python3 setup.py install

install-user: build
	python3 setup.py install --user

git:
	git push --all
	git push --tags

check:
	python3 setup.py check

# dist:
# 	python3 setup.py sdist upload -r pypi
# 	python3 setup.py bdist_wheel upload

docs:
	sphinx-apidoc -d 6 -e -f -o docs monitor
	make -C docs clean html

release: clean check dist git
