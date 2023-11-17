
restart_server:
	uvicorn objstore:app --reload --port 8001

run_client:
	python main.py

test:
	# tests from tests folder
	cd tests/; pytest test_*.py



