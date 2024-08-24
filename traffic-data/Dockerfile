# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the traffic-data directory contents into the container
COPY ./traffic-data/ ./traffic-data/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r ./traffic-data/requirements.txt

# Set the working directory to the traffic-data folder
WORKDIR /app/traffic-data

# Run the script when the container launches
CMD ["python" , "run_pipeline.py"]