.PHONY: all manual-build manual-upload-to-testpypi manual-upload-to-pypi test

all: manual-build

manual-build:
	@python -m build

manual-upload-to-testpypi:
	@python -m twine upload --repository testpypi dist/streamingjson-$(VERSION)*

manual-upload-to-pypi:
	@python -m twine upload --repository pypi dist/streamingjson-$(VERSION)*

test:
	@python -m tox
