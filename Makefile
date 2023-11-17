
dev_server:
	uvicorn objstore:app --reload --port 8001

start_server:
	python -m objstore server --host localhost --port 8000

test_client:
	python -m objstore list --host localhost --port 8000

test: uninstall
	# NOTE: you'll need to have a running server by this point
	# tests from tests folder
	cd tests/; pytest test_*.py


PACKAGE_NAME = objstore
PACKAGE_FOLDER = $(PACKAGE_NAME)/
build:
	# install latest version of compiler software
	pip install --user --upgrade setuptools wheel
	
	# actually set up package
	python setup.py sdist bdist_wheel
	
	git add setup.cfg setup.py LICENSE

install:
	pip install --upgrade .

uninstall:
	pip uninstall $(PACKAGE_NAME)
	
clean:
	-rm -r $(PACKAGE_NAME).egg-info
	-rm -r dist
	-rm -r build



