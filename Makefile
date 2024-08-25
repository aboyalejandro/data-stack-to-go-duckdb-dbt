# Check if docker-compose is available, otherwise use docker compose
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null || echo "docker compose")

.PHONY: build run clean

# Run the Docker container
run:
	docker compose up --build

# Stop and remove the container, image and generated files
clean:
	docker compose down --rmi all --volumes --remove-orphans
	find ./traffic-data/files -mindepth 1 ! -name '.gitkeep' -delete
	find ./website-analytics/traffic_data.duckdb  -delete

# Connect back to duckdb 
duckdb files:
	docker cp dbt-traffic-data-website_analytics-1:app/traffic-data/files/traffic_data.duckdb ./website-analytics/traffic_data.duckdb
	docker cp dbt-traffic-data-website_analytics-1:app/traffic-data/files/query.csv ./traffic-data/files/query.csv
	docker cp dbt-traffic-data-website_analytics-1:app/traffic-data/files/events.csv ./traffic-data/files/events.csv
	docker cp dbt-traffic-data-website_analytics-1:app/traffic-data/files/sessions.csv ./traffic-data/files/sessions.csv
	(cd website-analytics && duckdb traffic_data.duckdb)