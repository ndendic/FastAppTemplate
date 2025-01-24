# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set the working directory in the container
WORKDIR /src

# Copy only the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run on container start
CMD ["uv", "run", "src/main.py"]

