.PHONY: install test upload docs


install:
	pip install -e .[docs,test]

test:
	py.test

retest:
	py.test -vvv --lf

coverage:
	py.test --cov=wagtail_site_inheritance --cov-report=term-missing --cov-report=html

docs:
	$(MAKE) -C docs html

format:
	black --target-version=py36 --exclude=migrations .

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*
