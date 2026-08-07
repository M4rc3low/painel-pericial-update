.PHONY: test lint local worker clean

test:
	PYTHONPATH=src pytest -q

lint:
	ruff check src tests infra/lambda

local:
	docker compose up --build

worker:
	docker compose --profile worker run --rm worker

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache
