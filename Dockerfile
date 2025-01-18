# Start from the official slim Python 3.11 image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /flask_form

# Copy only the necessary files for dependency installation
COPY pyproject.toml poetry.lock ./

# Update package lists, install required system dependencies, and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy the remaining project files to the container
COPY . .

# Use Gunicorn as the application server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
