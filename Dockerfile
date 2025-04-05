# Use an official Python runtime as the base image for the backend
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install `uv` package manager
RUN pip install uv

# Copy backend files
COPY apps/backend/ ./

# Copy project files needed for dependency installation
COPY pyproject.toml ./
COPY uv.lock ./
COPY ./emergencyCentres.json ./

# Create a virtual environment using uv
RUN uv venv .venv

# Install dependencies using `uv sync`
RUN uv sync --python=.venv/bin/python

# Expose backend port
EXPOSE 8000

# Set Python path to include current directory
ENV PYTHONPATH=/app

# Start backend using the Python from the virtual environment
CMD ["/bin/sh", "-c", ".venv/bin/python src/utils/seed.py && .venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000"]
