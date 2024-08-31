# Check if docker-compose is available, otherwise use docker compose
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null || echo "docker compose")

.PHONY: build run clean duckdb_files

# Build the Docker container
build:
	$(DOCKER_COMPOSE) build

# Run the Docker container
run:
	$(DOCKER_COMPOSE) up 

# Stop the Docker container
stop:
	$(DOCKER_COMPOSE) down 

# Function to get the container ID dynamically
GET_CONTAINER_ID := $(DOCKER_COMPOSE) ps -q reporting

# Connect back to duckdb 
duckdb-files:
	$(eval CONTAINER_ID := $(shell $(GET_CONTAINER_ID)))
	@echo "Copying files from container..."
	docker cp $(CONTAINER_ID):/app/traffic-data/files/traffic_data.duckdb ./website-analytics/traffic_data.duckdb
	docker cp $(CONTAINER_ID):/app/traffic-data/files/. ./traffic-data/files/ && rm -f ./traffic-data/files/traffic_data.duckdb
	$(DOCKER_COMPOSE) down
	@echo "Activating DuckDB instance..."
	(cd website-analytics && duckdb traffic_data.duckdb)

# Stop and remove the container, image and generated files
clean:
	@echo "Removing all generated files..."
	$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
	find ./traffic-data/files -mindepth 1 ! -name '.gitkeep' -delete
	find ./website-analytics -name 'traffic_data.duckdb' -delete
	find ./reporting/exports -mindepth 1 ! -name '.gitkeep' -delete
	rm -f .DS_Store