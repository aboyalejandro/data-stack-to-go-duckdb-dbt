# Check if docker-compose is available, otherwise use docker compose
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null || echo "docker compose")

.PHONY: build run clean duckdb_files

# Build the Docker container
build:
	$(DOCKER_COMPOSE) build

# Run the Docker container
run:
	$(DOCKER_COMPOSE) up 

# Function to get the container ID dynamically
GET_CONTAINER_ID := $(DOCKER_COMPOSE) ps -q reporting

# Connect back to duckdb 
duckdb-files:
	$(eval CONTAINER_ID := $(shell $(GET_CONTAINER_ID)))
	docker cp $(CONTAINER_ID):/app/traffic-data/files/traffic_data.duckdb ./website-analytics/traffic_data.duckdb
	docker cp $(CONTAINER_ID):/app/traffic-data/files/query.csv ./traffic-data/files/query.csv
	docker cp $(CONTAINER_ID):/app/traffic-data/files/events.csv ./traffic-data/files/events.csv
	docker cp $(CONTAINER_ID):/app/traffic-data/files/sessions.csv ./traffic-data/files/sessions.csv
	$(DOCKER_COMPOSE) down

# Connect to duckdb 
duckdb:
	(cd website-analytics && duckdb traffic_data.duckdb)

# Stop and remove the container, image and generated files
clean:
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	find ./traffic-data/files -mindepth 1 ! -name '.gitkeep' -delete
	find ./website-analytics -name 'traffic_data.duckdb' -delete
	find ./reporting/exports -mindepth 1 ! -name '.gitkeep' -delete
	rm -f .DS_Store