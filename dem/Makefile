.PHONY: docker_up docker_down docker_build

docker_up:
	docker compose -f ./docker-compose.yml down
	docker compose -f ./docker-compose.yml up

docker_down:
	docker compose -f ./docker-compose.yml down

docker_build:
	docker compose -f ./docker-compose.yml build

# Helper command to view logs
docker_logs:
	docker compose logs -f

# Clean up everything, including volumes
docker_clean:
	docker compose down -v --remove-orphans 