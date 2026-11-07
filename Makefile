
.PHONY: lint lint_fix test check

lint:
	docker compose exec -T django uv run --no-sync ruff check .
	docker compose exec -T django uv run --no-sync ruff format --check .
	docker compose exec -T react npm run lint
	docker compose exec -T react npm run format:check

lint_fix:
	docker compose exec -T django uv run --no-sync ruff check . --fix
	docker compose exec -T django uv run --no-sync ruff format .
	docker compose exec -T react npm run lint -- --fix
	docker compose exec -T react npm run format

test:
	docker compose exec -T django uv run --no-sync pytest
	docker compose exec -T react npm run test

check: lint test
