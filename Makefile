ruff:
	poetry run ruff check --fix

run:
	poetry run uvicorn api.src.main:app --port 3000