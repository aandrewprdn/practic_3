ruff:
	poetry run ruff format

run-api:
	poetry run fastapi dev ./api/src/main.py --port 3000

run-ui:
	poetry run python ui/src/launch.py