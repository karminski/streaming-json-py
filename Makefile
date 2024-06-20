.PHONY: build all test clean

all: build 

manual-build: python -m build

manual-upload-to-testpypi:
	python -m twine upload --repository testpypi dist/*

manual-upload-to-pypi:
	python -m twine upload --repository pypi dist/*

run-tox:
	python -m tox
