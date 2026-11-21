.PHONY: lint lint_fix typecheck test check

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

typecheck:
	docker compose exec -T django uv run --no-sync mypy .
	docker compose exec -T react npm run typecheck

test:
	docker compose exec -T django uv run --no-sync pytest
	docker compose exec -T react npm run test

check: lint typecheck test

routes:
	docker compose exec -T django uv run --no-sync python manage.py show_urls