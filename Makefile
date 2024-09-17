install:
	poetry install
gendiff:
	poetry run gendiff
build:
	poetry build
publish:
	poetry publish --dry-run	
lint:
	poetry run flake8 gendiff
package-install:
	python3 -m pip install --force-reinstall dist/hexlet_code-0.1.0-py3-none-any.whl
build-install:
	poetry install
	poetry build
	python3 -m pip install --force-reinstall dist/hexlet_code-0.1.0-py3-none-any.whl