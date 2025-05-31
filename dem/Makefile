.PHONY: docker_up docker_down docker_build

docker_up:
	docker-compose up

docker_down:
	docker-compose down

docker_build:
	docker-compose build

# Helper command to view logs
docker_logs:
	docker-compose logs -f

# Clean up everything, including volumes
docker_clean:
	docker-compose down -v --remove-orphans 