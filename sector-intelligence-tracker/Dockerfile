FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for psycopg2 and other tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the API port
EXPOSE 8000

# Set PYTHONPATH to include the current directory
ENV PYTHONPATH=/app

# Command to run migrations and then start the server
CMD alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port 8000
