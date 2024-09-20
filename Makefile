.PHONY: build all manual-build manual-upload-to-testpypi manual-upload-to-pypi test

all: manual-build 

manual-build: python -m build

manual-upload-to-testpypi:
	python -m twine upload --repository testpypi dist/*

manual-upload-to-pypi:
	python -m twine upload --repository pypi dist/*

test:
	python -m tox
