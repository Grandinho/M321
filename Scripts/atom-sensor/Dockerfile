# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install Flask requests

# Copy the current directory contents into the container at /app
COPY ./app /app

# Make port 2023 available to the world outside this container
EXPOSE 2101

# Define environment variable

# Run app.py when the container launches
CMD ["python", "app.py"]