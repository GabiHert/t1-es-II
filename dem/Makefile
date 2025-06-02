.PHONY: docker_up docker_down docker_build docker_logs docker_clean

docker_up:
	# docker compose -f ./build/docker-compose.yml down
	docker compose -f ./build/docker-compose.yml up

docker_down:
	docker compose -f ./build/docker-compose.yml down

docker_build:
	docker compose -f ./build/docker-compose.yml build

# Helper command to view logs
docker_logs:
	docker compose -f ./build/docker-compose.yml logs -f

# Clean up everything, including volumes
docker_clean:
	docker compose -f ./build/docker-compose.yml down -v --remove-orphans 