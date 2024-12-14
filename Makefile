# Сборка и запуск всех контейнеров
run-all:
	docker compose up -d --build --force-recreate

# Сборка и запуск api
run-api:
	docker compose up api -d --build --force-recreate

# Остановка и удаление всех контейнеров
down:
	docker compose down

# Запуск тестов и остановка сервисов
run-tests:
	docker compose up --build --force-recreate test