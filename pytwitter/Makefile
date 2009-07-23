# Generic makefile for python projects
# nsheridan@gmail.com (Niall Sheridan)

VER=$(shell python setup.py --version)
PROJECT=$(shell python setup.py --name)

default:
	$(MAKE) build

upload:
	python setup.py sdist upload

%:
	python setup.py $@

clean:
	python setup.py $@
	-rm -fr build dist

