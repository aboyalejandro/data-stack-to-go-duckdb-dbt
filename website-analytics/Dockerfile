# Use the official dbt Docker image as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy ALL folders
COPY . .

# Export ENV vars
ENV INPUT_FILES_PATH=${INPUT_FILES_PATH}
ENV DUCKDB_PATH=${DUCKDB_PATH}
ENV PYTHONDONTWRITEBYTECODE=1 

# Set the working directory to /website-analytics
WORKDIR /app/website-analytics

# Install dependencies
RUN pip install --upgrade pip
RUN pip install dbt-duckdb

# Command to run when starting the container
CMD ["sh", "-c", "dbt deps && dbt build && tail -f /dev/null"]
