run_client:
	poetry run python client/main.py

run_api:
	poetry run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	poetry run black .
	poetry run ruff check . --fix

test:
	poetry run pytest --cov .
	rm -f test_db.db