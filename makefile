.PHONY: clean build run up down status test lint

# Основные цели
clean:
	docker-compose down

build:
	docker-compose build

run: clean build up

up:
	docker-compose up -d

down:
	docker-compose down

# Дополнительные цели
status:
	docker-compose ps

logs:
	docker-compose logs -f

# Очистка контейнеров и образов Docker
clean-containers:
	docker-compose down -v --rmi all --remove-orphans

clean-images:
	docker rmi $(docker images -q)

# Проверка синтаксиса и форматирования Makefile
lint:
	make --dry-run --warn-undefined-variables

# Запуск тестов (если применимо)
test:
	# Замените на команду для запуска ваших тестов
	pytest

# Цель по умолчанию
.DEFAULT_GOAL := help

help:
	@echo "Makefile для управления Docker Compose"
	@echo ""
	@echo "Основные цели:"
	@echo "  make clean      Остановить и удалить контейнеры"
	@echo "  make build      Построить образы Docker"
	@echo "  make run        Очистить, построить и запустить контейнеры"
	@echo "  make up         Запустить контейнеры"
	@echo "  make down       Остановить и удалить контейнеры"
	@echo ""
	@echo "Дополнительные цели:"
	@echo "  make status     Показать статус контейнеров"
	@echo "  make logs       Показать логи контейнеров"
	@echo "  make clean-containers  Очистить все контейнеры"
	@echo "  make clean-images      Очистить все образы"
	@echo "  make lint       Проверить синтаксис и форматирование Makefile"
	@echo "  make test       Запустить тесты"
	@echo ""
	@echo "Цель по умолчанию: help"
