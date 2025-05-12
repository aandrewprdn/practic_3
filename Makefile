ruff:
	poetry run ruff check --fix

run-api:
	poetry run uvicorn api.src.main:app --port 3000
run-ui:
	poetry run python ui/src/launch.py