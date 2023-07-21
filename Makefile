help:
	@echo "nox - trigger nox build"
	@echo "clean - remove all build/python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"

nox:
	nox

docs:
	nox -s docs

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr deb_dist/
	rm -fr coverage-reports/
	rm -fr *.egg-info
	rm -fr *.tar.gz
	rm -fr .tox
	rm -fr .coverage
	rm -fr .cache
	rm -fr .pytest_cache
	find . -name '__pycache__' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

upload_pypi:
	python3 -m build
	echo "Use username __token__ and the upload token as password starting with pypi-"
	python3 -m twine upload dist/*

