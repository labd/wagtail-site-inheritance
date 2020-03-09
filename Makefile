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
	isort --recursive src tests
	black src/ tests/

#
# Utility
makemessages:
	cd src/wagtail_site_inheritance && python ../../manage.py makemessages -all

compilemessages:
	cd src/wagtail_site_inheritance && python ../../manage.py compilemessages

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*

exampledata:
	./manage.py migrate
	./manage.py loaddata demo/exampledata/auth_users.json
	./manage.py loaddata demo/exampledata/sites.json


dumpdata:
	./manage.py dumpdata wagtailcore wagtaildocs wagtailimages wagtail_site_inheritance \
	--exclude wagtailcore.grouppagepermission \
	--exclude wagtailcore.groupcollectionpermission \
	--exclude wagtailcore.collection \
	--exclude wagtailimages.rendition \
	--indent=4 --natural-foreign > demo/exampledata/sites.json
