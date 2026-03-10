# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY index.html .
COPY movie.html .

# Create directory for persistent storage
RUN mkdir -p /app/data

# Set environment variable for Flask
ENV FLASK_APP=main.py
ENV PYTHONUNBUFFERED=1

# Expose port 8080 (GCP Cloud Run default)
EXPOSE 8080

# Run the application with gunicorn for production
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app