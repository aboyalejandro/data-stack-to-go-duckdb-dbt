# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Avoid __pycache__
ENV PYTHONDONTWRITEBYTECODE=1

# Copy the reporting directory contents into the container
COPY ./reporting/ ./reporting/
COPY ./traffic-data/requirements.txt ./reporting/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./reporting/requirements.txt

# Set the working directory to the reporting folder
WORKDIR /app/reporting