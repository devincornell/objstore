
dev_server:
	uvicorn objstore:app --reload --port 8001

start_server:
	python -m objstore server --host localhost --port 8000

test_client:
	python -m objstore list --host localhost --port 8000

test:
	# NOTE: you'll need to have a running server by this point
	# tests from tests folder
	cd tests/; pytest test_*.py





