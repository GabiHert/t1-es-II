.PHONY: up down build logs clean help

help:
	@echo "Available commands:"
	@echo "  make up      - Start all services in detached mode"
	@echo "  make down    - Stop and remove all containers"
	@echo "  make build   - Rebuild all services"
	@echo "  make logs    - Show logs from all services"
	@echo "  make clean   - Stop containers and remove volumes"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build --no-cache

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f 